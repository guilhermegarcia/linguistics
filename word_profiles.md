# Word profiles

This very simple function ```profile()``` takes a string and returns its CV template. You can pre-specify the inventory (the example below also contains glides). For example:

```profile("bakaton")``` returns ```CVCVCVC```    

```profile("ba-ka-ton")``` returns ```CV.CV.CVC```   

Thus, you need to provide the syllabification in the input if you want it in the output.


```{Python}

vowels = ["a", "e", "i", "o", "u", "E", "O"]

glides = ["j", "w"]

consonants = ["b", "d", "f", "g", "k", "l", "L", "m", "n", "p", "r", "s", "S", "t", "v", "x", "z", "Z", "N", "L"]


def profile(word):
    
    output = ""

    for letter in word:
        if letter in consonants:
            output = output + "C"
        elif letter in glides:
            output = output + "G"
        elif letter in vowels:
            output = output + "V"
        else:
            if letter == "'":
                output = output
            elif letter == "-":
                output = output + "."
    
    return(output)
    
    


```
