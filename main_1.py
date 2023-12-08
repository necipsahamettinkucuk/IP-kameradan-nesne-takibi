import Camera_1

import AI_1
import torch as t
import torch.version

print(t.__version__)

print(torch.cuda.is_available())

if torch.cuda.is_available():
    print("Cuda is Availabe")
else:
    print("Cuda Can't be found")
print(torch.version.cuda)

c = Camera_1.Cam()

# AI nesnesini ve modelin kendisini yükle
# önceden eğittimiz yapay zeka ağını
ai = AI_1.Model(r"C:\Users\necip\Desktop\baba\ai_model\weights\ust.pt")

c.read_with_ai(ai)
