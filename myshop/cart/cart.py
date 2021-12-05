from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):    
    # Inicializa o carrinho de compras
    def __init__(self, request):        
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        # Salva um carrinho vazio na sessão
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart


    # Adiciona um produto no carrinho ou atualiza sua quantidade
    def add(self, product, quantity=1, override_quantity=False):        
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity

        self.save()


    # Marca a sessão como modificada para garantir qie ela seja salva
    def save(self):        
        self.session.modified = True


    # Remove um produto do carrinho de compras
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()


    # Itera pelos itens do carrinho de compras e obtem os produtos do banco de dados
    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item


    # Contabiliza todos os itens que estão no carrinho de compras
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())


    # Calcula custo total dos itens do carrinho
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    # Remove o carrinho da sessão
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
