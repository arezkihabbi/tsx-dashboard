from typing import Dict


def generate_docstring(description: str, methods: Dict[str, dict]):
    doc = [
        description,
        "",
        "    Methods",
        "    -------",
    ]

    for method_name, method_desc in methods.items():
        doc.append(f"    {method_name}")

        for param, desc in method_desc["args"].items():
            doc.append(f"        {param}")
            if "description" in desc:
                doc.append(f"            {desc['description']}")
            if "default" in desc:
                doc.append(f"            default: {repr(desc['default'])}")
            doc.append("")

    return "\n".join(doc)
