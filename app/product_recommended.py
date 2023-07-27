# from .models import Product
# from collections import Counter
# from sklearn.neighbors import NearestNeighbors

# import numpy as np

# def get_item_recommendations(cart, num_recommendations=5):
    

#     return []

    # # Extract the product IDs from the cart dictionary
    # product_ids = list(cart.keys())

    # # Convert the product IDs to integers
    # product_ids = [int(product_id) for product_id in product_ids]

    # print("Product IDs in cart:", product_ids)

    # # Get interactions of all users with the given product IDs
    # user_interactions = UserInteraction.objects.filter(product__id__in=product_ids)

    # print("User Interactions:", user_interactions)

    # # Create an interaction matrix (user x product) with counts of interactions
    # interaction_matrix = user_interactions.values('user__id', 'product__id').annotate(interaction_count=Count('id')).values_list('interaction_count', 'user__id', 'product__id')

    # # Convert the interaction matrix to a dictionary
    # interaction_dict = {}
    # for count, user_id, product_id in interaction_matrix:
    #     if user_id not in interaction_dict:
    #         interaction_dict[user_id] = {}
    #     interaction_dict[user_id][product_id] = count

    # # Convert the interaction dictionary to a list of lists (user x product matrix)
    # user_product_matrix = []
    # for user_id, items in interaction_dict.items():
    #     row = [items.get(product_id, 0) for product_id in product_ids]
    #     user_product_matrix.append(row)

    # # Perform k-NN to find most similar users (k=5 in this case)
    # k = min(5, len(user_product_matrix))
    # if k < 1:
    #     k = 1
    # knn = NearestNeighbors(n_neighbors=k, metric='cosine')
    # knn.fit(user_product_matrix)

    # # Find the nearest neighbors to the current user based on their interactions
    # user_cart_interaction = [cart.get(str(product_id), 0) for product_id in product_ids]
    # if not any(user_cart_interaction):
    #     # Handle the case when the cart is empty or no interactions are found
    #     user_cart_interaction = np.zeros(len(product_ids))
    # else:
    #     user_cart_interaction = np.array(user_cart_interaction).reshape(-1, 1)  # Convert to a 2D numpy array

    # similar_users = knn.kneighbors(user_cart_interaction.T, return_distance=False)[0]

    # # Get the product IDs of items recommended by the similar users
    # recommended_product_ids = []
    # for user_index in similar_users:
    #     for i, count in enumerate(user_product_matrix[user_index]):
    #         if count > 0 and product_ids[i] not in product_ids:
    #             recommended_product_ids.append(product_ids[i])

    # print("Recommended Product IDs (from k-NN):", recommended_product_ids)

    # # Fetch the recommended products from the database
    # recommended_products = Product.objects.filter(id__in=recommended_product_ids)

    # # Filter recommended products by the same subcategory
    # if product_ids:
    #     cart_products = Product.objects.filter(id__in=product_ids)
    #     cart_subcategories = cart_products.values_list('subcategory__name', flat=True).distinct()

    #     recommended_products = recommended_products.filter(subcategory__name__in=cart_subcategories)
    # else:
    #     # If the cart is empty, show some generic recommendations or handle it as desired.
    #     # For example, you can set a default subcategory to show recommendations for that.
    #     # recommended_products = Product.objects.filter(subcategory__name='Default Subcategory')
    #     recommended_products = Product.objects.none()  # This will show an empty list of recommendations.

    # print("Recommended Products (after filtering by subcategory):", recommended_products)

    # return recommended_products



# from .models import Product

# def get_item_recommendations(cart, num_recommendations=5):
#     product_ids = list(cart.keys())
#     # Convert the product IDs to integers
#     product_ids = [int(product_id) for product_id in product_ids]

#     # Get the subcategories of products in the cart
#     cart_subcategories = set(Product.objects.filter(id__in=product_ids).values_list('subcategory__name', flat=True))

#     # Find other products in the same subcategories as those in the cart
#     recommended_products = Product.objects.filter(subcategory__name__in=cart_subcategories).exclude(
#         id__in=product_ids
#     ).distinct()

#     # Rank the recommendations (you can customize this based on popularity, ratings, etc.)
#     recommended_products = recommended_products.order_by('-popularity')[:num_recommendations]

#     return recommended_products
