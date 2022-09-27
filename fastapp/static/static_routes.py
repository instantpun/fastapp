# =====================================
# Serving Static HTML - The Manual Way
# =====================================
# import pathlib
# current_dir = pathlib.Path(__file__).parent.resolve()
# @app.get("/")
# def read_root():
#     with open(f"{current_dir}/hello.html", "r") as f:
#         response = f.read()
#     if isinstance(response, bytes):
#         reponse = response.decode("utf-8")
#     return response