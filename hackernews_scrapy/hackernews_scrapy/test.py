from goose3 import Goose
g = Goose()
article = g.extract(url="https://github.com/thlorenz/learnuv") 
#article = g.extract(url="http://edition.cnn.com/2012/02/22/world/europe/uk-occupy-london/index.html?hpt=ieu_c2")
print(article.cleaned_text[:100])
