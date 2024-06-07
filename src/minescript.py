import re

class Lexer:
    def __init__(self, code):
        self.code = code

    def execute(self):
        lines = []
        for i in self.code.splitlines():
            if i.startswith(" "):
                lines.append(i.strip())
            if i.startswith("#"):
                pass
            else:
                lines.append(i)
        return "\n".join(lines)

class Parser:
    def __init__(self, code):
        self.code = code

    def execute(self):
        output = []
        current_command = ""
        inside_if = False
        for i in self.code.splitlines():
            if not i:
                continue
            elif i.startswith("if"):
                if current_command:
                    output.append(current_command)
                    current_command = ""
                current_command = self.parse_if_statement(i)
                inside_if = True
            elif i.startswith("print"):
                print_command = self.parse_print_statement(i, inside_if)
                if inside_if:
                    current_command += print_command
                    output.append(current_command)
                    current_command = ""
                    inside_if = False
                else:
                    output.append(print_command)
            elif i.startswith("kill"):
                kill_command = self.parse_kill_statement(i, inside_if)
                if inside_if:
                    current_command += kill_command
                    output.append(current_command)
                    current_command = ""
                    inside_if = False
                else:
                    output.append(kill_command)
            elif i.startswith("ban"):
                ban_command = self.parse_ban_statement(i, inside_if)
                if inside_if:
                    current_command += ban_command
                    output.append(current_command)
                    current_command = ""
                    inside_if = False
                else:
                    output.append(ban_command)
        if current_command:
            output.append(current_command)
        return "\n".join(output)

    def parse_if_statement(self, statement):
        tokens = statement.split()
        command = "/execute if "
        in_then = False
        score = False

        for token in tokens:
            if token == "if":
                continue
            elif token.startswith("score"):
                if not score:
                    score = True
                    command += "score "
                parts = re.split(r"[():]", token)
                command += f"{parts[1]} {parts[2]} "
            elif token in ("<", ">", "<=", ">=", "=="):
                command += {"<": "< ", ">": "> ", "<=": "<= ", ">=": ">= ", "==": "matches "}[token]
            elif token == "then":
                command += "run "
                in_then = True
        
        return command

    def parse_print_statement(self, statement, inside_if):
        message = re.search(r'print\("(.+)"\)', statement).group(1)
        if inside_if:
            return f"say {message}"
        else:
            return f"/say {message}"
        
    def parse_ban_statement(self, statement, inside_if):
        message = re.search(r'ban\((.+)\)', statement).group(1)
        if inside_if:
            return f"ban {message}"
        else:
            return f"/ban {message}"

    def parse_kill_statement(self, statement, inside_if):
        message = re.search(r'kill\((.+)\)', statement).group(1)
        if message == "players":
            message = "@a"
        elif message == "entities":
            message = "@e"
        elif message == "nearest":
            message = "@p"
        elif message == "user":
            message = "@s"
        else:
            pass

        if inside_if:
            return f"kill {message}"
        else:
            return f"/kill {message}"

mycode = """
if score(Daylowww:money) < score(SalleDeValras:money) then
    ban(Daylowww)
end

if block(~ ~82 ~) is minecraft:diamond_block then
    print("Yeah")
end
"""

code = Parser(Lexer(mycode).execute()).execute()
print(code)
