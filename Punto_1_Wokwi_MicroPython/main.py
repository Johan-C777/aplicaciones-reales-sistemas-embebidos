from machine import Pin
import uasyncio as asyncio

BUTTON1_GPIO = 13
BUTTON2_GPIO = 14

LED1_GPIO = 25
LED2_GPIO = 26

class AsyncQueue:
    def __init__(self, maxsize=10):
        self.maxsize = maxsize
        self.data = []

    async def put(self, item):
        while len(self.data) >= self.maxsize:
            await asyncio.sleep_ms(1)

        self.data.append(item)

    async def get(self):
        while len(self.data) == 0:
            await asyncio.sleep_ms(1)

        return self.data.pop(0)

led1 = Pin(LED1_GPIO, Pin.OUT)
led2 = Pin(LED2_GPIO, Pin.OUT)

led1.value(0)
led2.value(0)

button1 = Pin(BUTTON1_GPIO, Pin.IN, Pin.PULL_UP)
button2 = Pin(BUTTON2_GPIO, Pin.IN, Pin.PULL_UP)

sensor_queue = AsyncQueue(10)

button1_flag = asyncio.ThreadSafeFlag()
button2_flag = asyncio.ThreadSafeFlag()

def button1_isr(pin):
    button1_flag.set()


def button2_isr(pin):
    button2_flag.set()


button1.irq(
    trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
    handler=button1_isr
)

button2.irq(
    trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING,
    handler=button2_isr
)

async def producer_task():
    count = 0

    while True:
        count += 1

        print("[PRODUCER] Sending sensor data:", count)

        await sensor_queue.put(count)

        print("[PRODUCER] Data sent successfully")

        await asyncio.sleep_ms(1000)

async def consumer_task():
    while True:
        received_val = await sensor_queue.get()

        print(
            "[CONSUMER] Received Sensor Data:",
            received_val
        )

async def button1_task():
    while True:
        await button1_flag.wait()

        # Debounce
        await asyncio.sleep_ms(20)

        button_state = button1.value()

        if button_state == 0:
            led1.value(1)
            print("[BUTTON 1] PRESSED -> LED1 ON")
        else:
            led1.value(0)
            print("[BUTTON 1] RELEASED -> LED1 OFF")

async def button2_task():
    while True:
        await button2_flag.wait()

        # Debounce
        await asyncio.sleep_ms(20)

        button_state = button2.value()

        if button_state == 0:
            led2.value(1)
            print("[BUTTON 2] PRESSED -> LED2 ON")
        else:
            led2.value(0)
            print("[BUTTON 2] RELEASED -> LED2 OFF")

# MAIN

async def main():
    print()
    print("========================================")
    print(" ESP32 MicroPython IPC Demonstration")
    print("========================================")

    print("[INIT] GPIO initialized")
    print("[INIT] Custom sensor queue created")
    print("[INIT] Button flags created")
    print("[INIT] Button interrupts attached")

    asyncio.create_task(producer_task())
    asyncio.create_task(consumer_task())
    asyncio.create_task(button1_task())
    asyncio.create_task(button2_task())

    print("[INIT] All tasks created")
    print("----------------------------------------")
    print("Button 1 : GPIO13")
    print("Button 2 : GPIO14")
    print("LED 1    : GPIO25")
    print("LED 2    : GPIO26")
    print("----------------------------------------")
    print("[READY] System ready!")

    while True:
        await asyncio.sleep_ms(1000)


asyncio.run(main())
