class Utils:
    @staticmethod
    def seconds_to_hms(seconds):
        """Konwertuje liczbę sekund (od północy lub innego punktu w czasie)
        na format hh:mm:ss (jako string).
        """
        godzina = seconds // 3600
        minuta = (seconds % 3600) // 60
        sekunda = seconds % 60
        return f"{godzina:02d}:{minuta:02d}:{sekunda:02d}"

