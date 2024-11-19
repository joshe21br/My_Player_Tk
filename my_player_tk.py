import os
import pygame
import time
import base64
import tkinter as tk
from tkinter import filedialog, messagebox
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image, ImageTk
from io import BytesIO

# Variáveis globais
playlist = []  # Lista para armazenar os arquivos de música
current_track_index = -1  # Índice da música atual na playlist
music_file = None  # Arquivo de música atual
is_playing_all = False  # Controle do modo Play All

# Função para inicializar o pygame mixer
def init_audio():
    pygame.mixer.init()

# Função para tocar a música
def play_music(music_file):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play(loops=0, start=0.0)
    pygame.mixer.music.set_endevent(pygame.USEREVENT)  # Ativa o evento de fim de música

# Função para pausar a música
def pause_music():
    pygame.mixer.music.pause()

# Função para parar a música
def stop_music():
    pygame.mixer.music.stop()

# Função para controle do volume
def set_volume(volume):
    pygame.mixer.music.set_volume(volume)

# Função para recarregar a música
def reload_music(music_file):
    stop_music()  # Para qualquer música tocando
    play_music(music_file)  # Recarrega e começa a tocar a nova música

# Função para obter a duração total da música (em segundos) usando mutagen
def get_music_duration(music_file):
    try:
        audio = MP3(music_file)  # Carrega o arquivo MP3 com mutagen
        return audio.info.length  # Retorna a duração total da música em segundos
    except Exception as e:
        print(f"Erro ao obter a duração da música: {e}")
        return 0

# Função para obter o tempo restante da música em formato mm:ss
def get_remaining_time(music_file):
    current_time = pygame.mixer.music.get_pos() / 1000  # Converter milissegundos para segundos
    total_time = get_music_duration(music_file)  # Duração total da música
    remaining_time = total_time - current_time  # Tempo restante
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    return f"{minutes:02}:{seconds:02}"

# Função para extrair a capa do álbum de um arquivo MP3
def get_album_art(music_file):
    try:
        audio = MP3(music_file, ID3=ID3)
        for tag in audio.tags.values():
            if isinstance(tag, APIC):
                return tag.data  # Retorna os dados da imagem do álbum
    except Exception as e:
        print(f"Erro ao extrair a capa do álbum: {e}")
    return None  # Retorna None se não encontrar uma capa

# Função para atualizar a capa do álbum na interface
def update_album_art(album_art_image_label):
    global playlist, current_track_index
    album_art_data = get_album_art(playlist[current_track_index])
    if album_art_data:
        image = Image.open(BytesIO(album_art_data))  # Agora funciona, pois BytesIO está importado
        image = image.resize((300, 200), Image.Resampling.LANCZOS)  # Correção aqui
        album_art_image = ImageTk.PhotoImage(image)
    else:
        # Se não houver capa, exibe uma imagem padrão
        image = Image.open("default_album_art.png")  # Caminho para a imagem padrão
        image = image.resize((300, 200), Image.Resampling.LANCZOS)  # Correção aqui
        album_art_image = ImageTk.PhotoImage(image)

    album_art_image_label.config(image=album_art_image)
    album_art_image_label.image = album_art_image

# Função para carregar a música e iniciar a reprodução
def on_file_selected():
    global playlist, current_track_index
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        playlist.append(file_path)
        current_track_index = len(playlist) - 1
        update_album_art(album_art_image_label)
        play_music(file_path)
        song_name_var.set(os.path.basename(file_path))
        update_time_label()
        update_playlist_display()

# Função para atualizar o tempo restante da música
def update_time_label():
    if current_track_index >= 0:
        time_left = get_remaining_time(playlist[current_track_index])
        time_label.config(text=time_left)
        root.after(1000, update_time_label)  # Atualiza a cada 1 segundo

# Funções de controle de música
def play():
    global is_playing_all
    if current_track_index >= 0:
        play_music(playlist[current_track_index])
        is_playing_all = False  # Desativa o modo Play All ao tocar uma música específica
        update_album_art(album_art_image_label)
        song_name_var.set(os.path.basename(playlist[current_track_index]))
        update_time_label()

def pause():
    pause_music()

def stop():
    stop_music()

# Função para controle de volume
def volume_changed(val):
    set_volume(float(val) / 100)  # Ajusta o volume

# Função para avançar para a próxima música
def next_song():
    global current_track_index
    if current_track_index < len(playlist) - 1:
        current_track_index += 1
        play_music(playlist[current_track_index])
        update_album_art(album_art_image_label)
        song_name_var.set(os.path.basename(playlist[current_track_index]))
        update_time_label()

# Função para retroceder para a música anterior
def previous_song():
    global current_track_index
    if current_track_index > 0:
        current_track_index -= 1
        play_music(playlist[current_track_index])
        update_album_art(album_art_image_label)
        song_name_var.set(os.path.basename(playlist[current_track_index]))
        update_time_label()

# Função para atualizar a lista de músicas na interface
def update_playlist_display():
    playlist_display.delete(1.0, tk.END)
    for index, song in enumerate(playlist):
        playlist_display.insert(tk.END, f"{index + 1}. {os.path.basename(song)}\n")

# Função para tocar toda a playlist
def play_whole_playlist():
    global current_track_index, is_playing_all
    current_track_index = 0
    is_playing_all = True  # Ativa o modo Play All
    play_music(playlist[current_track_index])
    update_album_art(album_art_image_label)
    song_name_var.set(os.path.basename(playlist[current_track_index]))
    update_time_label()

# Função para o duplo clique na playlist
def on_playlist_double_click(event):
    global current_track_index
    index = playlist_display.index(tk.CURRENT)
    current_track_index = int(index.split('.')[0]) - 1  # Ajusta o índice
    play_music(playlist[current_track_index])
    update_album_art(album_art_image_label)
    song_name_var.set(os.path.basename(playlist[current_track_index]))
    update_time_label()

# Função chamada quando a música termina, para tocar a próxima música
def music_ended():
    global current_track_index, is_playing_all
    if is_playing_all:
        if current_track_index < len(playlist) - 1:
            current_track_index += 1
            play_music(playlist[current_track_index])
            update_album_art(album_art_image_label)
            song_name_var.set(os.path.basename(playlist[current_track_index]))
            update_time_label()
        else:
            # Quando a playlist terminar, pode ser interessante parar a música
            print("Fim da playlist")
            stop_music()
            is_playing_all = False  # Desativa o modo Play All
    else:
        stop_music()  # Para a música se não estiver no modo Play All

# Função para verificar se a música terminou
def check_music_end():
    # Verifica se a música está tocando
    if not pygame.mixer.music.get_busy():  # Quando a música não está mais tocando
        music_ended()  # Chama a função para ir para a próxima música

    root.after(100, check_music_end)  # Verifica a cada 100ms

def clear_playlist():
    global playlist, current_track_index
    playlist = []  # Limpa a playlist
    current_track_index = -1  # Reseta o índice da música atual
    update_playlist_display()  # Atualiza a exibição da playlist
    song_name_var.set("Nenhuma música selecionada")  # Reseta o nome da música
    stop_music()  # Para qualquer música que esteja tocando
    # Verifica se a playlist está vazia antes de tentar atualizar a capa do álbum
    if current_track_index >= 0 and len(playlist) > 0:
        update_album_art(album_art_image_label)  # Limpa a capa do álbum
    else:
        album_art_image_label.config(image='')  # Se não houver músicas, limpa a imagem da capa


# Configuração da janela Tkinter
root = tk.Tk()
root.title("JOSHEBRK21")
root.geometry("800x650")  # Tamanho menor da janela
root.resizable(False, False)  # Impede o redimensionamento da janela
root.configure(bg="#2E3B4E")  # Cor de fundo mais escura

# Inicializando o áudio
init_audio()

# Variáveis de interface
song_name_var = tk.StringVar()

# Layout usando grid
frame_left = tk.Frame(root, width=200, bg="#2E3B4E", height=500)
frame_left.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

frame_right = tk.Frame(root, width=550, bg="#2E3B4E", height=500)
frame_right.grid(row=0, column=1, padx=10, pady=10, sticky="nswe")

# Título
title_label = tk.Label(frame_right, text="Joshe - Player",
                       font=("Helvetica", 16, "bold"),
                       fg="#FFFFFF",
                       bg="#2E3B4E")
title_label.grid(row=0, column=0, pady=5)

# Nome da música
song_name_label = tk.Label(frame_right, textvariable=song_name_var, font=("Helvetica", 14), fg="#FFFFFF", bg="#2E3B4E")
song_name_label.grid(row=2, column=0, pady=5)

# Seletor de arquivo
select_file_button = tk.Button(frame_right,
                               text="Selecionar Música",
                               font=("Helvetica", 12),
                               bg="#8BC34A", fg="white",
                               relief="flat",
                               command=on_file_selected, width=20)
select_file_button.grid(row=1, column=0, pady=10)

# Capa do álbum
album_art_image_label = tk.Label(frame_right, bg="#2E3B4E")
album_art_image_label.grid(row=3, column=0, pady=15)

# Controle de tempo
time_label = tk.Label(frame_right,
                      text="00:00",
                      font=("Helvetica", 12),
                      fg="#FFFFFF",
                      bg="#2E3B4E")
time_label.grid(row=4, column=0, pady=5)

# Playlist
playlist_label = tk.Label(frame_left,
                          text="Playlist",
                          font=("Helvetica", 14),
                          fg="white",
                          bg="#2E3B4E")
playlist_label.grid(row=0, column=0, pady=10)

playlist_display = tk.Text(frame_left,
                           width=30,
                           height=15,
                           font=("Helvetica", 10),
                           bg="#333333",
                           fg="white",
                           wrap="word",
                           bd=0)
playlist_display.grid(row=1, column=0, pady=10)

# Vincula o evento de duplo clique na playlist para tocar a música
playlist_display.bind("<Double-1>", on_playlist_double_click)

# Botões de controle
controls_frame = tk.Frame(frame_right, bg="#2E3B4E")
controls_frame.grid(row=5, column=0, pady=10)

play_button = tk.Button(controls_frame,
                        text="▷",
                        font=("Helvetica", 16),
                        bg="#4CAF50",
                        fg="white",
                        command=play,
                        relief="flat",
                        width=5)
play_button.grid(row=0, column=0, padx=5)

pause_button = tk.Button(controls_frame,
                         text="⏸",
                         font=("Helvetica", 16),
                         bg="#FFC107",
                         fg="white",
                         command=pause,
                         relief="flat",
                         width=5)
pause_button.grid(row=0, column=1, padx=5)

stop_button = tk.Button(controls_frame,
                        text="■",
                        font=("Helvetica", 16),
                        bg="#F44336",
                        fg="white",
                        command=stop,
                        relief="flat",
                        width=5)
stop_button.grid(row=0, column=2, padx=5)

previous_button = tk.Button(controls_frame,
                            text="◁",
                            font=("Helvetica", 16),
                            bg="#2196F3",
                            fg="white",
                            command=previous_song,
                            relief="flat",
                            width=5)
previous_button.grid(row=0, column=3, padx=5)

next_button = tk.Button(controls_frame,
                        text="▷",
                        font=("Helvetica", 16),
                        bg="#2196F3",
                        fg="white",
                        command=next_song,
                        relief="flat",
                        width=5)
next_button.grid(row=0, column=4, padx=5)

# Botão para tocar toda a playlist
play_all_button = tk.Button(frame_left,
                            text="Play All",
                            font=("Helvetica", 12),
                            bg="#8BC34A",
                            fg="white",
                            relief="flat",
                            command=play_whole_playlist)
play_all_button.grid(row=6, column=0, pady=10)

# Botão para limpar a playlist
clear_playlist_button = tk.Button(frame_left,
                                  text="Limpar Playlist",
                                  font=("Helvetica", 12),
                                  bg="#F44336",
                                  fg="white",
                                  relief="flat",
                                  command=clear_playlist)
clear_playlist_button.grid(row=7, column=0, pady=10)

# Volume (label + slider lado a lado)
volume_frame = tk.Frame(frame_right, bg="#2E3B4E")
volume_frame.grid(row=6, column=0, pady=10)

volume_label = tk.Label(volume_frame, text="Volume", font=("Helvetica", 12), fg="white", bg="#2E3B4E")
volume_label.grid(row=0, column=0, padx=5)

volume_slider = tk.Scale(volume_frame,
                         from_=0, to=100, orient="horizontal",
                         command=volume_changed, bg="#2E3B4E",
                         fg="white", sliderlength=20, length=200,
                         troughcolor="#4CAF50", activebackground="#8BC34A",
                         highlightthickness=0)
volume_slider.set(50)  # Valor inicial do volume
volume_slider.grid(row=0, column=1, padx=5)

# Rodapé com versão e contato
footer_label = tk.Label(root, text="Versão: 1.0 | Desenvolvedor: Joshe | Contato: josuesouzadasilva@gmail.com | (85)989780215",
                        font=("Helvetica", 10), fg="white", bg="#2E3B4E")
footer_label.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

# Rodando a aplicação
check_music_end()  # Inicia o monitoramento dos eventos de música
root.mainloop()

