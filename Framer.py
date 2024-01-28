import cv2
from screeninfo import Monitor, get_monitors
import os

fileName = "TillLindemannIchhasseKinderTheShortMovie.webm"
capture = cv2.VideoCapture(fileName)
while not capture.isOpened():
    capture = cv2.VideoCapture(fileName)
    cv2.waitKey(1000)
    print("Wait for the header")

KEY_ESC = 27
KEY_SPACE = 32
KEY_DELETE = 127
KEY_PLUS = 43
KEY_MINUS = 45
KEY_LEFT = ord("a")
KEY_UP = ord("w")
KEY_RIGHT = ord("d")
KEY_DOWN = ord("s")
KEY_H = ord("h")
KEY_Q = ord("q")
KEY_E = ord("e")
KEY_R = ord("r")
KEY_T = ord("t")
KEY_X = ord("x")

"""
isCurrentFrameRead, currentFrame = capture.read()
while 1:
    cv2.imshow("img", currentFrame)
    k = cv2.waitKey(1)
    if k == KEY_ESC:
        break
    elif k == -1:
        continue
    else:
        print(k)
"""

FRAME_NAME = "FRAME_NAME"

IS_STOPPED = False
IS_PRESSED_LEFT = False
IS_PRESSED_RIGHT = False
SHOW_INFO_ENABLED = True
SPEED = 1
NEXT_FRAME_COUNT = 1
TOTAL_FRAME_COUNT = capture.get(cv2.CAP_PROP_FRAME_COUNT)

PRIMARY_MONITOR = Monitor
for monitor in get_monitors():
    if monitor.is_primary:
        PRIMARY_MONITOR = monitor

isCurrentFrameRead = False
currentFrame = cv2.typing.MatLike
currentFramePosition = nextFramePosition = capture.get(cv2.CAP_PROP_POS_FRAMES)


def getFramePosition():
    return capture.get(cv2.CAP_PROP_POS_FRAMES)


def setFramePosition(nextFramePosition):
    capture.set(cv2.CAP_PROP_POS_FRAMES, nextFramePosition)


while True:
    pressedKey = cv2.waitKey(SPEED * 10)
    if pressedKey == KEY_ESC:
        break

    if pressedKey == KEY_SPACE:
        IS_STOPPED = not IS_STOPPED

    if pressedKey is KEY_RIGHT:
        IS_PRESSED_RIGHT = True
        nextFramePosition = currentFramePosition + NEXT_FRAME_COUNT

    if pressedKey is KEY_LEFT:
        IS_PRESSED_LEFT = True
        nextFramePosition = currentFramePosition - NEXT_FRAME_COUNT

    if pressedKey is KEY_H:
        SHOW_INFO_ENABLED = not SHOW_INFO_ENABLED

    if pressedKey is KEY_PLUS:
        SPEED = SPEED - 1
        if SPEED <= 0:
            SPEED = 1

    if pressedKey is KEY_MINUS:
        SPEED = SPEED + 1
        if SPEED > 1000:
            SPEED = 1000

    if pressedKey is KEY_Q:
        NEXT_FRAME_COUNT = NEXT_FRAME_COUNT - 1
        if NEXT_FRAME_COUNT < 0:
            NEXT_FRAME_COUNT = 1

    if pressedKey is KEY_E:
        NEXT_FRAME_COUNT = NEXT_FRAME_COUNT + 1
        if NEXT_FRAME_COUNT > 1000:
            NEXT_FRAME_COUNT = 1000

    if pressedKey is KEY_R:
        NEXT_FRAME_COUNT = 1

    if pressedKey is KEY_T:
        NEXT_FRAME_COUNT = 100

    if pressedKey is KEY_X:
        IS_STOPPED = True
        frameToBeTakenCount = 5
        outputFolder = fileName + " output"
        if not os.path.isdir(outputFolder):
            os.makedirs(outputFolder)
        for x in range(0, (frameToBeTakenCount * 2)):
            if x > frameToBeTakenCount:
                nextFramePosition = currentFramePosition - frameToBeTakenCount + x
            else:
                nextFramePosition = currentFramePosition - x
            setFramePosition(nextFramePosition)
            isCurrentFrameRead, currentFrame = capture.read()
            cv2.imwrite(
                f"{outputFolder}/{fileName.split('.')[0]}-{int(nextFramePosition)}.png",
                currentFrame,
            )

        setFramePosition(currentFramePosition)
        IS_STOPPED = False

    if currentFramePosition < nextFramePosition and IS_PRESSED_RIGHT:
        IS_PRESSED_RIGHT = not IS_PRESSED_RIGHT
        if TOTAL_FRAME_COUNT <= nextFramePosition:
            nextFramePosition = TOTAL_FRAME_COUNT - 1
        setFramePosition(nextFramePosition)

    if currentFramePosition > nextFramePosition and IS_PRESSED_LEFT:
        IS_PRESSED_LEFT = not IS_PRESSED_LEFT
        if nextFramePosition < 0:
            nextFramePosition = 0
        setFramePosition(nextFramePosition)

    if IS_STOPPED:
        setFramePosition(nextFramePosition)
    else:
        nextFramePosition = currentFramePosition

    currentFramePosition = getFramePosition()

    isCurrentFrameRead, currentFrame = capture.read()
    if not isCurrentFrameRead:
        setFramePosition(currentFramePosition - 1)
        print("Frame is not ready")
        cv2.waitKey(1000)
        continue

    cv2.namedWindow(FRAME_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(FRAME_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    # cv2.moveWindow(frameName, primaryMonitor.x, primaryMonitor.y)

    if SHOW_INFO_ENABLED:
        info = "Frame: " + str(currentFramePosition)
        infoX = 50
        infoY = 50
        cv2.putText(
            currentFrame,
            info,
            (infoX, infoY),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

        info = "Speed: " + str(SPEED)
        infoY += 50
        cv2.putText(
            currentFrame,
            info,
            (infoX, infoY),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

        info = "Next Frame Count: " + str(NEXT_FRAME_COUNT)
        infoY += 50
        cv2.putText(
            currentFrame,
            info,
            (infoX, infoY),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )

    cv2.imshow(
        FRAME_NAME,
        cv2.resize(currentFrame, (PRIMARY_MONITOR.width, PRIMARY_MONITOR.height)),
    )

    if currentFramePosition >= TOTAL_FRAME_COUNT - 1:
        currentFramePosition = TOTAL_FRAME_COUNT - (NEXT_FRAME_COUNT * SPEED)
        # break
