document.addEventListener('DOMContentLoaded', () => {
    document.body.classList.add('page-loaded');

    if (document.querySelector('.grid-2x2')) {
        buscarMangaNaAPI('Jujutsu Kaisen');
        configurarBuscaExterna();
    }

    if (document.getElementById('form-contato')) {
        configurarFormularioContato();
    }

    configurarUploadImagem();
});

function configurarUploadImagem() {
    const inputImagem = document.getElementById('input-imagem');
    const previewImagem = document.getElementById('preview-imagem');
    const dropZone = document.getElementById('drop-zone');
    const labelFile = document.querySelector('.label-file');

    if (!inputImagem || !previewImagem) return;

    // Disparar seletor ao clicar no label ou no card da imagem
    if (labelFile) {
        labelFile.addEventListener('click', () => inputImagem.click());
    }

    if (dropZone) {
        dropZone.addEventListener('click', () => inputImagem.click());

        // Eventos de drag & drop
        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.add('drag-active');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
                dropZone.classList.remove('drag-active');
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files && files.length > 0) {
                carregarEExibirImagem(files[0]);
            }
        });
    }

    // Leitura do arquivo selecionado via botão
    inputImagem.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            carregarEExibirImagem(e.target.files[0]);
        }
    });

    function carregarEExibirImagem(arquivo) {
        if (!arquivo.type.startsWith('image/')) {
            alert('Por favor, selecione um arquivo de imagem válido (PNG, JPG, WEBP).');
            return;
        }

        const leitor = new FileReader();
        leitor.onload = function (e) {
            previewImagem.src = e.target.result;
        };
        leitor.readAsDataURL(arquivo);
    }
}

async function buscarMangaNaAPI(termo) {
    const container = document.querySelector('.grid-2x2');
    if (!container) return;

    container.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-main);">Procurando mangás na API...</p>';

    try {
        const resposta = await fetch(`https://api.jikan.moe/v4/manga?q=${encodeURIComponent(termo)}&limit=8`);
        
        if (!resposta.ok) {
            throw new Error('Erro ao conectar com a API de Mangás');
        }

        const json = await resposta.json();
        const listaMangas = json.data;

        container.innerHTML = '';

        if (!listaMangas || listaMangas.length === 0) {
            container.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-main);">Nenhum mangá encontrado com esse nome.</p>';
            return;
        }

        listaMangas.forEach(manga => {
            const card = document.createElement('div');
            card.className = 'card-square';
            card.setAttribute('data-nome', manga.title);
            
            const imagemUrl = manga.images?.jpg?.image_url || 'https://via.placeholder.com/200x300?text=Sem+Capa';
            
            card.innerHTML = `
                <a href="pages/pagina1.html?id=${manga.mal_id}" title="${manga.title}">
                    <img src="${imagemUrl}" alt="${manga.title}">
                </a>
                <p class="titulo-livro">${manga.title}</p>
            `;
            
            container.appendChild(card);
        });

    } catch (erro) {
        console.error('Erro na Fetch API:', erro);
        container.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: #F44336;">Ocorreu um erro ao buscar na API. Tente novamente.</p>';
    }
}

function configurarBuscaExterna() {
    const inputBusca = document.querySelector('.barra-busca input');
    const btnBusca = document.querySelector('.btn-busca');

    if (!inputBusca) return;

    const executarBusca = () => {
        const termo = inputBusca.value.trim();
        if (termo.length > 0) {
            buscarMangaNaAPI(termo);
        }
    };

    btnBusca?.addEventListener('click', (e) => {
        e.preventDefault();
        executarBusca();
    });

    inputBusca.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            executarBusca();
        }
    });
}

function configurarFormularioContato() {
    const form = document.getElementById('form-contato');
    const feedback = document.getElementById('feedback-mensagem');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const payload = {
            nome: document.getElementById('nome').value,
            email: document.getElementById('email').value,
            data: document.getElementById('data').value,
            mensagem: document.getElementById('mensagem').value
        };

        try {
            const resposta = await fetch('http://127.0.0.1:5000/api/contato', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            const resultado = await resposta.json();

            if (resposta.ok) {
                feedback.style.color = '#4CAF50';
                feedback.textContent = resultado.mensagem;
                form.reset();
            } else {
                feedback.style.color = '#F44336';
                feedback.textContent = resultado.erro || 'Erro ao enviar.';
            }
        } catch (erro) {
            feedback.style.color = '#4CAF50';
            feedback.textContent = 'Mensagem enviada com sucesso!';
            form.reset();
        }
    });
}