from lighting_time_calculator import LightingTimeCalc


def main():
    newCalc = LightingTimeCalc()
    times = newCalc.getTimesToTurnLights()
    print(times[0])
    print(times[1])
    return 0


if __name__ == "__main__":
    main()
