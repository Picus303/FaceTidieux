from pydantic import BaseModel
from typing import Literal


BinaryChoice = Literal["Yes", "No", "Unknown"]
HairColorChoice = Literal["Black", "Brown", "Blond", "Unknown"]


class CNNRequest(BaseModel):
	Hair_Color: HairColorChoice
	Sideburns: BinaryChoice
	Bangs: BinaryChoice
	No_Beard: BinaryChoice
	Wearing_Necktie: BinaryChoice
	Big_Lips: BinaryChoice
	Wearing_Lipstick: BinaryChoice
	Straight_Hair: BinaryChoice
	Chubby: BinaryChoice
	Big_Nose: BinaryChoice
	Pointy_Nose: BinaryChoice
	Goatee: BinaryChoice
	Male: BinaryChoice
	Receding_Hairline: BinaryChoice
	Wearing_Necklace: BinaryChoice
	Eyeglasses: BinaryChoice
	Wavy_Hair: BinaryChoice
	Wearing_Earrings: BinaryChoice
	Young: BinaryChoice