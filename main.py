
from pwm_tester import PWMTester


def main():

    pwm_tester = PWMTester()
    pwm_tester.setup()

    while True:
        pwm_tester.loop()

        
if __name__ == "__main__":
    main()