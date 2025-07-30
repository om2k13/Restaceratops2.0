
import xml.etree.ElementTree as ET, time, pathlib

class JUnitReporter:
    def __init__(self, file_path="report.xml"):
        self.file_path = pathlib.Path(file_path)
        self.testsuite = ET.Element("testsuite", name="restaceratops")

    def record(self, step_name, success, latency_ms, error=None):
        case = ET.SubElement(self.testsuite, "testcase", name=step_name, time=str(latency_ms/1000))
        if not success:
            failure = ET.SubElement(case, "failure", message=str(error) or "failure")
            if error:
                failure.text = str(error)

    def write(self):
        tree = ET.ElementTree(self.testsuite)
        tree.write(self.file_path, encoding="utf-8", xml_declaration=True)
        return self.file_path
