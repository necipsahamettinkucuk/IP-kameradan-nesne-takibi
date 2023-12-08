import Camera_2
import AI_2
import torch as t
import torch.version

print(t.__version__)

print(torch.cuda.is_available())

if torch.cuda.is_available():
    print("Cuda is Availabe")
else:
    print("Cuda Can't be found")
print(torch.version.cuda)


c = Camera_2.Cam()

# AI nesnesini ve modelin kendisini yükle

ai = AI_2.Model(r"C:\Users\necip\Desktop\baba\ai_model\weights\ust.pt")

c.read_with_ai(ai)
