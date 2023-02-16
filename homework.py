M_IN_KM = 1000  # Meter to km.


class InfoMessage:
    """Информационное сообщение о тренировке."""
    pass


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # Length of the step in meters.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self, distance) -> float:
        """Получить среднюю скорость движения."""
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        pass


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    H_IN_MIN = 60  # Hours into minutes.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self, mean_speed) -> float:
        duration_in_min: int = self.duration * 60  # Training time in min.
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * mean_speed
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / M_IN_KM * duration_in_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1 = 0.035  # Coefficient for counting calories.
    K_2 = 0.029  # Coefficient for counting calories.
    KMH_IN_MS = 3.6  # Km/h to m/sec.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # Length of the stroke in meters.
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    commands = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    for command in commands:
        if workout_type is command:
            return commands[command](data)


def main(training: Training) -> None:
    """Главная функция."""
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
