import os
import pandas as pd
from dotenv import load_dotenv
from typing import List, Dict, Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

import sys
sys.path.append(os.path.dirname(__file__))
from products import get_df_by_category, ALL_CATEGORIES, Product, get_products_summary, get_categories_with_names

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.4
)

app = FastAPI(
    title="Smart Search Products (LangChain)",
    description="Assistente de compras inteligente."
)

@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Smart Search Products Backend is running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisResult(BaseModel):
    budget: Optional[float] = None
    categories: List[str]

class PromptRequest(BaseModel):
    prompt: str
    budget: Optional[float] = None

@app.post("/generate")
async def generate_text(request: PromptRequest):
    try:
        """ Análise de Intenção """
        parser = JsonOutputParser(pydantic_object=AnalysisResult)
        
        analysis_prompt = PromptTemplate(
            template="""Você é um analista de compras de uma loja estilo Amazon.
            Sua tarefa é analisar o pedido do usuário e mapear para as categorias CORRETAS do nosso banco de dados.
            
            Pedido: "{query}"
            Extraia o orçamento (budget) numérico se houver.
            
            Lista de Categorias Disponíveis (ID: Nome):
            {available_categories}
            
            REGRAS DE MAPEAMENTO:
            1. Se o produto solicitado (ex: Notebook) NÃO existir nas categorias (ex: não temos Laptops), NÃO tente forçar categorias irrelevantes como Celulares ou Eletrodomésticos apenas por serem tecnologia.
            2. Se não houver uma categoria que combine muito bem com o que foi pedido, retorne uma lista de categorias VAZIA [].
            3. Priorize precisão sobre quantidade.
            
            Retorne apenas JSON: {{"budget": float ou null, "categories": ["CategoriaID1", "CategoriaID2"]}}
            """,
            input_variables=["query", "available_categories"]
        )

        analysis_chain = analysis_prompt | llm | parser
        
        analysis_data = analysis_chain.invoke({
            "query": request.prompt,
            "available_categories": get_categories_with_names() # Enviamos ID e Nome Traduzido
        })
        
        max_price = request.budget or analysis_data.get("budget")
        relevant_categories = [cat for cat in analysis_data.get("categories", []) if cat in ALL_CATEGORIES]

        """ Busca de Dados Reais """
        context_data = ""
        if relevant_categories:
            for cat in relevant_categories[:5]: 
                summary = get_products_summary(cat, limit=18, max_price=max_price) # Aumentado para 10 itens por categoria
                context_data += summary + "\n"
        
        """ Geração da Resposta Final """
        budget_info = f" (com orçamento de até R$ {max_price})" if max_price else ""
        
        from products import translate_category
        relevant_cat_translated = translate_category(relevant_categories[0]) if relevant_categories else "nossas categorias"

        final_prompt = PromptTemplate(
            template="""Você é um assistente de compras inteligente da Amazon.
            Sua missão é analisar e dar um feedback sobre a busca: **{query}**{budget_info}.

            Dados reais do nosso estoque para esta consulta:
            {context}

            REGRAS OBRIGATÓRIAS DE FORMATAÇÃO E CONTEÚDO:
            1. SEM SAUDAÇÕES: É proibido usar "Olá", "Oi", etc. Comece direto.
            
            2. DESTAQUE DA BUSCA: Use sempre **negrito** (ex: **{query}**) e NUNCA use aspas.
            
            3. CATEGORIA: Se for mencionar a categoria, use o nome traduzido: **{relevant_category_name}**. NUNCA use aspas simples ou o nome em inglês (como 'Air Conditioners').
            
            4. PREÇOS: Comente sobre a faixa de preços encontrada e SEMPRE envolva os valores em símbolo de igual duplo (ex: ==R$ 50,00==).
            
            5. TEXTO: Escreva apenas um parágrafo direto (3 a 5 linhas). Proibido citar nomes de produtos ou marcas no texto.
            
            6. TAGS DE FILTRO (CRÍTICO): Sugira 3 termos curtos ao final. 
               - O formato DEVE ser exatamente: [FILTRO]Termo[/FILTRO]
               - NÃO coloque quebras de linha entre as tags. Todas devem estar na mesma linha ou em linhas limpas. 
               - NÃO escreva a palavra "[FILTRO]" sozinha antes dos termos.
            
            7. FORMATO [ITEM]: Logo após o parágrafo, liste os produtos usando as tags [ITEM].

            CASO A: SE encontrou produtos:
            - Texto analítico + Lista [ITEM] + Filtros no final.

            CASO B: SE for "NADA_ENCONTRADO":
            - Informe apenas que não há itens para **{query}**.

            [ITEM]
            NOME: [nome exato]
            PRECO: [preço em R$]
            RATING: [rating]
            IMAGEM: ![texto](url)
            [/ITEM]
            """,
            input_variables=["query", "context", "budget_info", "relevant_category_name"]
        )

        final_chain = final_prompt | llm
        
        response = final_chain.invoke({
            "query": request.prompt,
            "context": context_data if context_data else "NADA_ENCONTRADO",
            "budget_info": budget_info,
            "relevant_category_name": relevant_cat_translated
        })

        return {
            "response": response.content,
            "detected_budget": max_price,
            "queried_categories": relevant_categories
        }
    
    except Exception as e:
        print(f"Erro LangChain: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/categories")
async def get_categories():
    
    from products import translate_category
    return [{"id": cat, "name": translate_category(cat)} for cat in ALL_CATEGORIES]

@app.get("/products/{category}")
async def get_products_by_category(category: str, page: int = 1, page_size: int = 20):
    df = get_df_by_category(category)
    if df is None:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    
    total_products = len(df)
    total_pages = (total_products + page_size - 1) // page_size
    
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    
    df_slice = df.iloc[start_idx:end_idx].copy()
    
    from products import clean_price, INR_TO_BRL
    
    products_list = []
    for _, row in df_slice.iterrows():
        p = row.fillna("").to_dict()
        price_inr = clean_price(p.get('actual_price', '0'))
        p['actual_price'] = f"R$ {price_inr * INR_TO_BRL:.2f}"
        products_list.append(p)
        
    return {
        "products": products_list,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "total_products": total_products
    }