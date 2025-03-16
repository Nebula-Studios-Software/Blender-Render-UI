class CommandGenerator:
    def __init__(self):
        self.base_command = "blender"
        self.parameters = []

    def add_parameter(self, param):
        self.parameters.append(param)

    def remove_parameter(self, param):
        if param in self.parameters:
            self.parameters.remove(param)

    def generate_command(self):
        command = [self.base_command]
        command.extend(self.parameters)
        return " ".join(command)

    def clear_parameters(self):
        self.parameters.clear()