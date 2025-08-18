from dataclasses import dataclass


@dataclass
class Report:
    report_id: str
    description: str
    language: str

    @classmethod
    def from_dict(cls, datum: dict) -> "Report":
        return cls(
            report_id=datum.get("reportId"),
            description=datum.get("description"),
            language=datum.get("language"),
        )
