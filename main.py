from fastapi import FastAPI , BackgroundTasks
from pydantic import BaseModel , validator
import task

app = FastAPI()

languages = ["English" , "French", "German", "Romanian"]
class Translation(BaseModel):
    text : str
    base_lang : str
    final_lang : str

    @validator('base_lang','final_lang')
    def valid_lang(cls ,lang):
        if lang not in languages :
            raise ValueError("Invalid language")
        return lang


##Route 1:/
## Test if everthing is working
## {"message" : "Hello world"}

@app.get("/")
def get_root():
    return{"messge":"Hello World"}
## Route 2:/ translate
## Take in a translation request and store it to the db
## Return a Translation id
@app.post("/translate")
def post_translation(t: Translation , background_tasks:BackgroundTasks):
    #Store the translation
    #Run translation in background
    t_id = task.store_translation(t)
    background_tasks.add_task(task.run_translation ,t_id)
    return {"task_id":t_id}


## Route 3:/results
## Take in a translation id
## Return the translated text
@app.get("/results")
def get_translation(t_id:int):
    return {"translation": task.find_translation(t_id)}


