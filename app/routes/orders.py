from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Order, OrderItem, Product

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    """Get all orders for the current user"""
    try:
        user_id = int(get_jwt_identity())
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()

        return jsonify([order.to_dict() for order in orders]), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get a specific order"""
    try:
        user_id = int(get_jwt_identity())
        order = Order.query.get(order_id)

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Ensure the order belongs to the current user
        if order.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify(order.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    """Create a new order"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        # Validate required fields
        if not data or not data.get('items'):
            return jsonify({'error': 'Order items are required'}), 400

        # Validate items is a list and not empty
        if not isinstance(data['items'], list) or len(data['items']) == 0:
            return jsonify({'error': 'Order must contain at least one item'}), 400

        # Calculate total and validate products
        total = 0
        order_items = []

        for item in data['items']:
            # Validate item structure
            if not item.get('product_id') or not item.get('quantity'):
                return jsonify({'error': 'Each item must have product_id and quantity'}), 400

            # Validate quantity
            if item['quantity'] <= 0:
                return jsonify({'error': 'Quantity must be positive'}), 400

            # Get product
            product = Product.query.get(item['product_id'])
            if not product:
                return jsonify({'error': f'Product {item["product_id"]} not found'}), 404

            # Check stock availability
            if product.stock < item['quantity']:
                return jsonify({'error': f'Insufficient stock for product {product.name}'}), 400

            # Calculate item total
            item_total = product.price * item['quantity']
            total += item_total

            # Create order item
            order_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': product.price
            })

        # Create order
        order = Order(
            user_id=user_id,
            total=total,
            status='pending'
        )
        db.session.add(order)
        db.session.flush()  # Get order ID

        # Create order items and update stock
        for item_data in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item_data['product'].id,
                quantity=item_data['quantity'],
                price=item_data['price']
            )
            db.session.add(order_item)

            # Update product stock
            item_data['product'].stock -= item_data['quantity']

        db.session.commit()

        return jsonify({
            'message': 'Order created successfully',
            'order': order.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    """Update order status"""
    try:
        user_id = int(get_jwt_identity())
        order = Order.query.get(order_id)

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Ensure the order belongs to the current user
        if order.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()

        # Update status if provided
        if 'status' in data:
            valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
            if data['status'] not in valid_statuses:
                return jsonify({'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}), 400
            order.status = data['status']

        db.session.commit()

        return jsonify({
            'message': 'Order updated successfully',
            'order': order.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@orders_bp.route('/<int:order_id>', methods=['DELETE'])
@jwt_required()
def cancel_order(order_id):
    """Cancel an order (restores product stock)"""
    try:
        user_id = int(get_jwt_identity())
        order = Order.query.get(order_id)

        if not order:
            return jsonify({'error': 'Order not found'}), 404

        # Ensure the order belongs to the current user
        if order.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        # Only allow cancellation of pending orders
        if order.status != 'pending':
            return jsonify({'error': 'Only pending orders can be cancelled'}), 400

        # Restore product stock
        for item in order.items:
            product = Product.query.get(item.product_id)
            if product:
                product.stock += item.quantity

        # Update order status
        order.status = 'cancelled'
        db.session.commit()

        return jsonify({'message': 'Order cancelled successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
