from .models import Category, Product, Brand, UserInteraction
from datetime import datetime
from collections import Counter



def get_item_recommendations(cart, num_recommendations=5):
    product_ids = list(cart.keys())

    # Convert the product IDs to integers
    product_ids = [int(product_id) for product_id in product_ids]

    print("Product IDs in cart:", product_ids)

    products = Product.objects.filter(id__in=product_ids)
    sub_categories = products.values_list('subcategory', flat=True)
    recommended_products = Product.objects.filter(subcategory__in=sub_categories).exclude(
        id__in=products
    )[:5]
    return recommended_products

    # Get interactions of all users with the given product IDs
    user_interactions = UserInteraction.objects.filter(product__id__in=product_ids)

    print("User Interactions:", user_interactions)

    # Calculate similarity between users based on their interactions
    user_similarity = {}
    for interaction in user_interactions:
        user_id = interaction.user.id
        product_id = interaction.product.id

        if user_id not in user_similarity:
            user_similarity[user_id] = Counter()

        user_similarity[user_id][product_id] += 1

    # Find users most similar to the current user based on their interactions
    most_similar_users = Counter()
    for user_id, items in user_similarity.items():
        most_similar_users.update(items)

    # Exclude products already in the cart from recommendations
    for product_id in product_ids:
        most_similar_users[product_id] = 0

    # Get the recommended product IDs
    recommended_product_ids = [product_id for product_id, _ in most_similar_users.most_common(num_recommendations)]

    print("Recommended Product IDs:", recommended_product_ids)

   
    recommended_products = Product.objects.filter(id__in=recommended_product_ids)

    
    cart_products = Product.objects.filter(id__in=product_ids)
    cart_brands = set(cart_products.values_list('brand__name', flat=True))
    cart_categories = set(cart_products.values_list('category__name', flat=True))
    cart_subcategories = set(cart_products.values_list('subcategory__name', flat=True))

    recommended_products = recommended_products.filter(
        brand__name__in=cart_brands,
        category__name__in=cart_categories,
        subcategory__name__in=cart_subcategories,
    )

    print("Recommended Products:", recommended_products)

    return recommended_products
