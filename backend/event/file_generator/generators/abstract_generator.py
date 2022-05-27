from abc import ABC, abstractmethod
from openpyxl import Workbook

from event.file_generator.models import GeneratedFiles


class AbstractGenerator(ABC):

    def __init__(self, generated_file: GeneratedFiles):
        super().__init__()
        self.generated_file = generated_file

    @abstractmethod
    def generate(self) -> Workbook:
        pass
