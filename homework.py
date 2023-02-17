M_IN_KM = 1000  # Meter to km.
H_IN_MIN = 60  # Hours into minutes.


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

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self, mean_speed) -> float:
        duration_in_min: int = self.duration * H_IN_MIN  # Training time in
        # minutes.
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

    def get_spent_calories(self, mean_speed) -> float:
        mean_speed_in_ms = mean_speed / self.KMH_IN_MS  # Speed km/h to m/s.
        duration_in_min: int = self.duration * H_IN_MIN  # Training time in
        # minutes.
        return ((self.K_1 * self.weight + (mean_speed_in_ms**2 / self.height)
                 * self.K_2 * self.weight) * duration_in_min)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # Length of the stroke in meters.

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    
    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self, mean_speed) -> float:
        return (mean_speed + 1.1) * 2 * self.weight * self.duration


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
