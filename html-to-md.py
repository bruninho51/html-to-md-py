import re
import os
import tempfile
import subprocess
import sys

def add_pre_tag_around_code_tag(html_content):
    modified_html = re.sub(r'<code class="([^"]*)">([^<]*)</code>', r'<pre><code class="\1">\2</code></pre>', html_content)
    return modified_html

def modify_html_file(html_file):
    # Ler o conteúdo do arquivo HTML
    with open(html_file, 'r') as f:
        html_content = f.read()

    # Fazer a substituição no conteúdo HTML
    modified_html = add_pre_tag_around_code_tag(html_content)

    # Escrever o conteúdo modificado em um arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.html')
    temp_file.write(modified_html)
    temp_file.close()

    return temp_file.name

def convert_html_to_markdown(html_file):
    # Pasta do arquivo HTML
    html_folder = os.path.dirname(html_file)
    
    # Nome do arquivo Markdown
    markdown_file = os.path.splitext(html_file)[0] + '.md'

    # Usa o Pandoc para converter o arquivo HTML para Markdown
    command = [
        "pandoc",
        "-t", "markdown-simple_tables-multiline_tables-grid_tables",
        "--wrap=none",
        "--columns=999",
        "-s", "-o", markdown_file,
        html_file
    ]
    subprocess.run(command)

    # Lê o conteúdo do arquivo Markdown gerado
    with open(markdown_file, 'r') as f:
        markdown_content = f.read()

    return markdown_content

def format_code_tag_content(markdown_content):
    # Remover espaços extras, mantendo a identação
    code_blocks = re.findall(r'```.*?```', markdown_content, re.DOTALL)
    for block in code_blocks:
        lines = block.split('\n')
        if lines:
            # Calcula o número de espaços à esquerda na primeira linha
            spaces_to_remove = len(lines[1]) - len(lines[1].lstrip())
            # Remove espaços extras de todas as linhas intermediárias, mantendo a identação
            trimmed_lines = [lines[0]] + [line[spaces_to_remove:] for line in lines[1:-1]] + [lines[-1]]
            trimmed_block = '\n'.join(trimmed_lines)
            markdown_content = markdown_content.replace(block, trimmed_block)

    return markdown_content

def modify_md_file(markdown_content):
    markdown_content = format_code_tag_content(markdown_content)

    return markdown_content

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py path/to/html_file")
        sys.exit(1)

    # Caminho do arquivo HTML de entrada
    html_file = sys.argv[1]

    # Modificar o arquivo HTML e obter o nome do arquivo temporário
    temp_html_file = modify_html_file(html_file)

    # Converte o HTML para Markdown e devolve o conteúdo
    markdown_content = convert_html_to_markdown(temp_html_file)

    # Modifica o Markdown devolvendo o conteúdo da versão final
    final_markedown_content = modify_md_file(markdown_content)

    # Nome do arquivo Markdown de saída
    markdown_file = os.path.splitext(html_file)[0] + '.md'
    
    # Salvar o conteúdo do Markdown final no arquivo .md
    with open(markdown_file, 'w') as f:
        f.write(final_markedown_content)

    print(f"Markdown gerado e salvo em '{markdown_file}'")
