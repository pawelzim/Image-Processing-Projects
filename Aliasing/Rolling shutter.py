import cv2

def aliasing(videoCap, l):
    width = int(videoCap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(videoCap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(videoCap.get(cv2.CAP_PROP_FPS))

    success, stoppedFrame = videoCap.read()

    # Sprawdzenie, czy plik zostal wgrany poprawnie
    # Wypisanie rozdzielczosci wczytanego pliku oraz fps
    if success:
        print("Successful video read")
        print("Height: ", height)
        print("Width: ", width)
        print("FPS: ", fps)
    else:
        print("Unsuccessful video read")
        quit()

    # Wartosc wysokosci jest "limitem" dzialania funkcji
    framesLimit = height

    # Tworzenie pliku "out", do ktorego zapisany bedzie stworzony film .mp4
    out = cv2.VideoWriter()
    out.open('fan_5_16l.mp4', cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps, (width, height), True)
    success, currentFrame = videoCap.read()
    framesRead = 0

    while success and (framesRead <= framesLimit):
        # Nadpisanie wszystkich klatek kolejnymi, poza zatrzymanymi
        stoppedFrame[framesRead:-1, :] = currentFrame[framesRead:-1, :]
        out.write(stoppedFrame)
        # Przypisywanie za kazdym razem kolejnych klatek pliku
        success, currentFrame = videoCap.read()
        framesRead += l

    if not success:
        print("Finished")
    else:
        print("Finished 2")

# -------------------------------------------------------

l = int(input("Wpisz l: "))
# ponizej sciezka do pliku .mp4/.gif
videoCap = cv2.VideoCapture('')

aliasing(videoCap, l)
