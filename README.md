# AlugaFácil

Plataforma web desenvolvida em Django para intermediação de aluguéis de imóveis residenciais e comerciais, conectando proprietários anunciantes a inquilinos interessados.

A documentação completa do projeto (escopo, regras de negócio, modelagem conceitual, casos de uso e arquitetura) está disponível no diretório `docs/`.

## Tecnologias Utilizadas

* Python
* Django
* python-dotenv
* Pillow
* Bootstrap e Font Awesome
* SQLite3

## Instalação e Execução Local

1. **Clone o repositório e acesse o diretório:**
   ```bash
   git clone [https://github.com/RennerRSouza/AlugaFacil.git](https://github.com/RennerRSouza/AlugaFacil.git)
   cd alugafacil
   ```

2. **Crie e ative o ambiente virtual:**

   **Windows (CMD):**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

   **Linux:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```

5. **Crie um superusuário (Admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

7. **Acesse no navegador:**
   * `http://127.0.0.1:8000/`
