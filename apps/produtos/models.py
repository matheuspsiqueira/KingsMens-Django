from django.db import models

class Produto(models.Model):
    nome_produto = models.CharField(max_length=200)
    categoria = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    imagem1 = models.ImageField(upload_to='', blank=True)
    imagem2 = models.ImageField(upload_to='', blank=True)
    def __str__(self):
        return self.nome_produto


class ItemCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    preco_total = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade} x {self.produto.nome_produto}"

    def save(self, *args, **kwargs):
        self.preco_total = self.quantidade * self.preco_unitario
        super(ItemCarrinho, self).save(*args, **kwargs)

def excluir_item_carrinho(self):
    self.delete()