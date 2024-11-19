# My Player Tk

O **My Player Tk** é um reprodutor de música simples e eficiente desenvolvido em Python. Utilizando bibliotecas como `pygame` para reprodução de áudio, `mutagen` para manipulação de arquivos MP3 e `tkinter` para criar a interface gráfica, o My Player Tk permite que você gerencie uma playlist, toque suas músicas favoritas e visualize informações como a capa do álbum e o tempo restante da música.

## Funcionalidades

- **Reprodução de Música**: Toque, pause, pare e navegue entre as músicas da playlist.
- **Controle de Volume**: Ajuste o volume da música em tempo real.
- **Exibição de Capa de Álbuns**: Mostra a capa do álbum (caso disponível no arquivo MP3).
- **Playlist**: Gerencie sua lista de músicas, incluindo a capacidade de adicionar músicas à playlist.
- **Modo Play All**: Toque todas as músicas da playlist de forma contínua.
- **Tempo Restante**: Mostra o tempo restante da música atualmente em reprodução.
- **Interface Simples**: Interface gráfica intuitiva utilizando `tkinter` para facilitar o uso.

## Requisitos

Antes de executar o My Player Tk, você precisa garantir que as seguintes bibliotecas estejam instaladas:

- `pygame` — Para reprodução de áudio.
- `mutagen` — Para manipulação de tags e metadados de arquivos MP3.
- `PIL` (Pillow) — Para exibir imagens, como a capa do álbum.
- `tkinter` — Para a interface gráfica (já incluída na instalação padrão do Python).

Você pode instalar as dependências com o seguinte comando:

```bash
pip install pygame mutagen pillow
```

## Como Executar

1. Clone este repositório ou baixe o arquivo `my_player_tk.py`.
2. Instale as dependências (caso não tenha feito ainda):
   
   ```bash
   pip install pygame mutagen pillow
   ```

3. Execute o aplicativo:

   ```bash
   python my_player_tk.py
   ```

4. Utilize a interface gráfica para carregar músicas, tocar, pausar, ajustar volume e visualizar a capa do álbum.

## Como Funciona

- O player usa o **pygame** para carregar e tocar arquivos MP3.
- A **mutagen** é utilizada para extrair informações da música, como a duração e a capa do álbum.
- O **tkinter** cria a interface do usuário onde você pode visualizar a música, a capa do álbum e a playlist.
- O aplicativo permite que você adicione músicas à playlist, controle a reprodução (play, pause, stop), e visualize informações como o tempo restante.

## Estrutura do Projeto

```plaintext
- my_player_tk.py           # Arquivo principal com o código do reprodutor
- default_album_art.png     # Imagem padrão para capas de álbum (se não houver capa no arquivo MP3)
```

## Interface Gráfica

O layout da interface é simples e direto, com a separação entre a área de controle da playlist (à esquerda) e a área de controle de música e visualização (à direita):

- **Seleção de Música**: Um botão para selecionar arquivos MP3 e adicioná-los à playlist.
- **Capa do Álbum**: Exibe a capa do álbum da música atual ou uma imagem padrão.
- **Controles de Música**: Botões para tocar, pausar, parar, e navegar entre as músicas.
- **Volume**: Um controle deslizante para ajustar o volume da música.
- **Tempo**: Exibe o tempo restante da música atual.

## Funções Principais

- **`play_music(music_file)`**: Toca a música selecionada.
- **`pause_music()`**: Pausa a música atual.
- **`stop_music()`**: Para a música atual.
- **`set_volume(volume)`**: Ajusta o volume da música.
- **`update_album_art(album_art_image_label)`**: Atualiza a capa do álbum na interface.
- **`get_remaining_time(music_file)`**: Retorna o tempo restante da música em formato MM:SS.
- **`play_whole_playlist()`**: Toca todas as músicas na playlist.
- **`clear_playlist()`**: Limpa a playlist e para qualquer música em reprodução.

## Exemplo de Uso

1. **Adicionar músicas**: Clique no botão "Selecionar Música" para carregar arquivos MP3 e adicioná-los à playlist.
2. **Reproduzir música**: Clique no botão "▷" para tocar a música atual. O nome da música e a capa do álbum serão exibidos.
3. **Controlar a música**: Use os botões de "⏸" (pausar), "■" (parar), "◁" (anterior) e "▷" (próxima) para controlar a reprodução.
4. **Ajuste de volume**: Use o controle deslizante para ajustar o volume da música.
5. **Modo Play All**: Clique no botão "Play All" para reproduzir todas as músicas da playlist.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

## Desenvolvedor

- **Joshe**
- **E-mail**: josuesouzadasilva@gmail.com  

## Agradecimentos

Agradecimentos especiais às bibliotecas **pygame**, **mutagen**, **Pillow** e **tkinter** por fornecerem as funcionalidades necessárias para a construção deste reprodutor de músicas!

