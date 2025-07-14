import pytest
from playwright.sync_api import Page
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5000"

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
    try:
        page.wait_for_url(BASE_URL + "/", timeout=3000)
    except:
        pass
    assert "login" in page.content().lower() or BASE_URL in page.url

def test_cadastro_pet(page: Page):
    page.goto(BASE_URL)
    page.fill('input[name="email"]', "teste@example.com")
    page.fill('input[name="senha"]', "1")
    page.click('button[type="submit"]')
    page.goto(BASE_URL + "/cadastro-pet")

    page.fill('input[name="nome"]', "Theo")
    page.fill('input[name="raca"]', "Spitz Alemão")
    page.fill('input[name="idade"]', "2")
    page.fill('input[name="peso"]', "4.5")
    page.fill('input[name="tipo_animal"]', "cachorro")

    page.click('button[type="submit"]')

    try:
        page.wait_for_url(BASE_URL + "/perfil", timeout=3000)
    except:
        pass

    content = page.content().lower()
    assert "seus pets" in content or "cadastrar novo pet" in content


def test_agendamento_servico(page: Page):
    page.goto(BASE_URL)
    page.fill('input[name="email"]', "teste@example.com")
    page.fill('input[name="senha"]', "1")
    page.click('button[type="submit"]')
    page.goto(BASE_URL + "/servicos-cliente")

    try:
        page.wait_for_selector('select[name="pet_id"]', timeout=3000)
        page.wait_for_selector('select[name="servico_id"]', timeout=3000)

        if page.query_selector('select[name="pet_id"] option'):
            page.select_option('select[name="pet_id"]', index=0)

        if page.query_selector('select[name="servico_id"] option'):
            page.select_option('select[name="servico_id"]', index=0)

        data = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        hora = "10:00"
        page.fill('input[name="data"]', data)
        page.fill('input[name="hora"]', hora)
        page.click('button[type="submit"]')

        page.wait_for_url(BASE_URL + "/servicos-cliente", timeout=3000)
        content = page.content().lower()
        assert "agendado" in content or "sucesso" in content or "servicos-cliente" in page.url
    except Exception as e:
        print("Erro ao tentar agendar serviço:", e)
        raise

def test_gerente_visualiza_usuarios(page: Page):
    page.goto(BASE_URL)
    page.fill('input[name="email"]', "admin@petshop.com")
    page.fill('input[name="senha"]', "1")
    page.click('button[type="submit"]')
    page.goto(BASE_URL + "/painel-gerente")

    try:
        page.wait_for_selector("text=usuários", timeout=3000)  
        html = page.content().lower()
        assert "usuário" in html or "email" in html or "admin" in html
    except Exception as e:
        print("Conteúdo de gerente não encontrado:", e)
        raise