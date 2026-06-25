import cv2
import time
import sys
from PIL import Image
import os
import tkinter as tk
# Desactivar el prompt de pygame antes de importarlo
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import fpstimer
import moviepy.editor as mp

try:
    ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "/", "=", "_", "·", " "]
    frame_size = 150

    frame_size_windows = 280

    ASCII_LIST = []


    def play_audio(path):
        pygame.init()
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()


    def play_video(total_frames):
        # Ajustar dimensiones de la consola (Ancho 150, Alto 500)
        os.system('mode 150, 500')

        # \033[2J limpia la pantalla, \033[?25l oculta el cursor de la terminal
        sys.stdout.write("\033[2J\033[?25l")
        sys.stdout.flush()

        timer = fpstimer.FPSTimer(30)

        # Reproducir fotogramas usando la cantidad real procesada
        for frame_number in range(len(ASCII_LIST)):
            # \033[H mueve el cursor a la esquina superior izquierda sin parpadeos
            sys.stdout.write("\033[H" + ASCII_LIST[frame_number])
            sys.stdout.flush()
            timer.sleep()

        # Volver a mostrar el cursor al finalizar la reproducción
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()


    # Modo Ventana
    def play_video_window():
        root = tk.Tk()

        # =========================
        # Ventana basica
        # =========================
        root.title("Ventana")
        root.configure(bg="black")

        # Toda la ventana grande
        root.state("zoomed")
        root.lift()
        root.attributes("-topmost", True)
        root.after(200, lambda: root.attributes("-topmost", False))
        root.focus_force()

        # =========================
        # Zona de contenido
        # =========================
        label = tk.Label(
            root,
            text="",
            fg="white",
            bg="black",
            justify="left",
            anchor="nw",
            font=("Consolas", 10),
        )
        label.pack(fill="both", expand=True)

        # =========================
        # Notificacion en cargar
        # =========================
        loading_label = tk.Label(
            root,
            text="Cargando ASCII Video...",
            fg="white",
            bg="black",
            font=("Consolas", 28, "bold")
        )
        loading_label.place(relx=0.5, rely=0.5, anchor="center")

        root.update_idletasks()
        root.update()

        frame_index = 0

        # =========================
        # Simplificar la letra
        # =========================
        def resize_font(event=None):
            width = root.winfo_width()
            height = root.winfo_height()

            # tamaño
            font_size = max(
                8,
                min(
                    int(width / 95),
                    int(height / 55)
                )
            )

            label.config(font=("Consolas", font_size))

        root.bind("<Configure>", resize_font)

        # =========================
        # Evitar que se parezca en modo pequeño
        # =========================
        def prevent_minimize(event=None):
            if root.state() == "iconic":
                root.after(1, lambda: root.state("zoomed"))

        root.bind("<Unmap>", prevent_minimize)

        # =========================
        # maximizar
        # =========================
        scale_factor = max(1, frame_size_windows // frame_size)

        def enlarge_frame(frame):
            lines = frame.split("\n")

            return "\n".join(
                "".join(char * scale_factor for char in line)
                for line in lines
            )

        # =========================
        # actualizar obligatoriamente
        # =========================
        root.update_idletasks()
        root.update()

        # Eliminar la carga
        loading_label.destroy()

        # =========================
        # demostrar el primer pixel
        # =========================
        if len(ASCII_LIST) > 0:
            first_frame = enlarge_frame(ASCII_LIST[0])
            label.config(text=first_frame)

        root.update()

        # =========================
        # Reproducir el audio
        # =========================
        play_audio("audio.mp3")

        # =========================
        # Actualizacion del pixel
        # =========================
        def update_frame():
            nonlocal frame_index

            frame_start = time.time()

            if frame_index < len(ASCII_LIST):

                enlarged_frame = enlarge_frame(
                    ASCII_LIST[frame_index]
                )

                label.config(text=enlarged_frame)

                frame_index += 1

                # =========================
                # FPS en modo igual
                # =========================
                elapsed = (time.time() - frame_start) * 1000

                delay = max(1, int(33 - elapsed))

                root.after(delay, update_frame)

            else:
                root.destroy()

        resize_font()
        update_frame()
        root.mainloop()

        sys.exit()


    # Extraer fotogramas del video
    def extract_transform_generate(video_path, start_frame, number_of_frames=1000):
        capture = cv2.VideoCapture(video_path)
        capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)  # Propiedad oficial de OpenCV para apuntar al frame

        frame_count = 1

        while frame_count <= number_of_frames:
            ret, image_frame = capture.read()
            if not ret:
                break
            try:
                # OpenCV lee en BGR, lo convertimos a RGB para que PIL procese los grises correctamente
                image_frame_rgb = cv2.cvtColor(image_frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image_frame_rgb)

                ascii_characters = pixels_to_ascii(greyscale(resize_image(image)))
                pixel_count = len(ascii_characters)

                ascii_image = "\n".join(
                    [ascii_characters[index:(index + frame_size)] for index in range(0, pixel_count, frame_size)])

                ASCII_LIST.append(ascii_image)

            except Exception as error:
                frame_count += 1
                continue

            progress_bar(frame_count, number_of_frames)
            frame_count += 1

        capture.release()
        sys.stdout.write('\n')  # Salto de línea limpio al finalizar la carga


    # Barra de progreso optimizada
    def progress_bar(current, total, barLength=25):
        progress = float(current) * 100 / total
        arrow = '#' * int(progress / 100 * barLength)
        spaces = ' ' * (barLength - len(arrow))
        sys.stdout.write('\rProgreso: [%s%s] %d%% Fotograma %d de %d' % (arrow, spaces, progress, current, total))
        sys.stdout.flush()


    # Redimensionar imagen manteniendo proporción en terminal
    def resize_image(image_frame):
        width, height = image_frame.size
        aspect_ratio = (height / float(width * 2.5))  # Multiplicador 2.5 compensa la escala vertical de la consola
        new_height = int(aspect_ratio * frame_size)
        resized_image = image_frame.resize((frame_size, new_height))
        return resized_image


    # Escala de grises
    def greyscale(image_frame):
        return image_frame.convert("L")


    # Convertir píxeles a caracteres ASCII
    def pixels_to_ascii(image_frame):
        pixels = image_frame.getdata()
        characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
        return characters


    def preflight_operations(path):
        if os.path.exists(path):
            path_to_video = path.strip()
            cap = cv2.VideoCapture(path_to_video)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            cap.release()

            # Extraer el audio del video e inicializarlo
            sys.stdout.write('Extrayendo pista de audio...\n')
            video = mp.VideoFileClip(path_to_video)
            path_to_audio = 'audio.mp3'
            video.audio.write_audiofile(path_to_audio, logger=None)  # Ocultar logs pesados de moviepy

            start_time = time.time()
            sys.stdout.write('Iniciando generación de ASCII...\n')

            # Limpiamos la lista global por si se ejecuta el reproductor varias veces
            ASCII_LIST.clear()

            # Procesamos secuencialmente de manera estable todos los fotogramas
            extract_transform_generate(path_to_video, 0, total_frames)
            execution_time = time.time() - start_time
            sys.stdout.write('Generación completada en: ' + str(round(execution_time, 2)) + ' segundos.\n')

            return total_frames
        else:
            sys.stdout.write('¡Error! Archivo de video no encontrado.\n')
            return None


    def main():
        while True:
            try:
                print("==============================================================\n")
                print('Seleccione una opción: ')
                print('1) Reproducir Video')
                print('2) Auto - video existente con el nombre video.mp4')
                print("3) Ejecutar en la Ventana")
                print("4) Salir \n")
                print('==============================================================\n')
                user_input = str(input("Tu opción: ")).strip()

                if user_input == '1':
                    video_name = str(input("Introduce el nombre del archivo de video: ")).strip()
                    total_frames = preflight_operations(f"{video_name}.mp4 ")
                    if total_frames:
                        play_audio('audio.mp3')
                        play_video(total_frames=total_frames)
                    else:
                        print("\nError en la ejecución - codigo 01\n")
                elif user_input == '2':
                    total_frames = preflight_operations(f"video.mp4")
                    if total_frames:
                        play_audio('audio.mp3')
                        play_video(total_frames=total_frames)
                    else:
                        print("\nError en la ejecución - codigo 02\n")
                elif user_input == "3":
                    print("\n======== Modo ventana =======\n")
                    video_name = str(input("Introduce el nombre del archivo de video: ")).strip()
                    total_frames = preflight_operations(f"{video_name}.mp4 ")
                    if total_frames:
                        play_video_window()
                    else:
                        print("\nError en la ejecución - codigo 03\n")
                    pass #codigo para que salga en la ventana en vez del terminal - aún falta

                elif user_input == "4":
                    sys.exit()

                else:
                    print("Buscando...")
                    time.sleep(1)
                    print('\n Opción desconocida, Vuelva a intentarlo \n')
                    time.sleep(1)
            except FileNotFoundError:
                print("No existe el archivo. ")


    if __name__ == '__main__':
        main()
        exit()

except KeyboardInterrupt:
    print("\n\n Ejecucion finalizado. ")
