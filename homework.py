M_IN_KM = 1000  # Meter to km.
H_IN_MIN = 60  # Hours into minutes.


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration}; '
                f'Дистанция: {self.distance}; '
                f'Ср. скорость: {self.speed}; '
                f'Потрачено ккал: {self.calories}.')


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

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        duration_in_min: float = self.duration * H_IN_MIN  # Training time in
        # minutes.
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight
                / M_IN_KM * duration_in_min)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    K_1 = 0.035  # Coefficient for counting calories.
    K_2 = 0.029  # Coefficient for counting calories.
    KMH_IN_MS = 3.6  # Km/h to m/sec.
    CM_IN_M = 100  # Centimetres to meters

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_speed_in_ms = self.get_mean_speed() / self.KMH_IN_MS  # Speed
        # conversion from km/h to m/s.
        duration_in_min: float = self.duration * H_IN_MIN  # Training time in
        # minutes.
        return ((self.K_1 * self.weight + (mean_speed_in_ms**2 / self.height
                 / self.CM_IN_M) * self.K_2 * self.weight) * duration_in_min)


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

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + 1.1) * 2 * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    commands = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    for command in commands:
        if workout_type is command:
            return commands[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
