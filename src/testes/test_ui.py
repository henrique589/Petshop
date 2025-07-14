import pytest
from playwright.sync_api import Page
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5000/"

@pytest.mark.parametrize("email,senha,tipo_esperado,url_destino", [
    ("admin@petshop.com", "1", "gerente", "/painel-gerente"),
])

def test_login_redireciona_para_painel(page: Page, email, senha, tipo_esperado, url_destino):
    page.goto(BASE_URL)
    page.fill('input[name="email"]', email)
    page.fill('input[name="senha"]', senha)
    page.click('button[type="submit"]')

    page.wait_for_url(f"**{url_destino}")
    assert url_destino in page.url

def test_cadastro_cliente(page: Page):
    page.goto(BASE_URL + "/cadastro")

    page.fill('input[name="nome"]', "Teste Playwright")
    page.fill('input[name="email"]', "teste@example.com")
    page.fill('input[name="senha"]', "1")
    page.fill('input[name="telefone"]', "11999999999")
    page.fill('input[name="cpf"]', "12345678900")

    page.click('button[type="submit"]')

    page.wait_for_url(BASE_URL + "/")
    assert "login" in page.content().lower() or BASE_URL in page.url

def test_cadastro_pet(page: Page):
    page.goto(BASE_URL)
    page.fill('input[name="email"]', "teste@example.com")
    page.fill('input[name="senha"]', "1")
    page.click('button[type="submit"]')

    page.goto(BASE_URL + "/cadastro-pet")

    page.fill('input[name="nome"]', "Theo")
    page.select_option('select[name="porte"]', "pequeno")
    page.select_option('select[name="especie"]', "cachorro")
    page.fill('input[name="raca"]', "Spitz Alemão")

    page.click('button[type="submit"]')

    page.wait_for_url(BASE_URL + "/perfil")
    assert "meus pets" in page.content().lower()

def test_agendamento_servico(page: Page):
    page.goto(BASE_URL)
    page.fill('input[name="email"]', "teste@example.com")
    page.fill('input[name="senha"]', "1")
    page.click('button[type="submit"]')

    page.goto(BASE_URL + "/servicos-cliente")

    page.wait_for_selector('select[name="pet_id"]')
    page.wait_for_selector('select[name="servico_id"]')

    page.select_option('select[name="pet_id"]', index=0)
    page.select_option('select[name="servico_id"]', index=0)

    data = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    hora = "10:00"

    page.fill('input[name="data"]', data)
    page.fill('input[name="hora"]', hora)

    page.click('button[type="submit"]')

    page.wait_for_url(BASE_URL + "/servicos-cliente")
    content = page.content().lower()
    assert "agendado" in content or "sucesso" in content or "servicos-cliente" in page.url

def test_gerente_visualiza_usuarios(page: Page):
    page.goto(BASE_URL)
    page.fill('input[name="email"]', "admin@petshop.com")
    page.fill('input[name="senha"]', "1")
    page.click('button[type="submit"]')

    page.goto(BASE_URL + "/painel-gerente")

    page.wait_for_selector("table")  

    html = page.content().lower()
    assert "nome" in html or "email" in html or "usuário" in html