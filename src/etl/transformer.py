from typing import Dict, List, Any, Tuple
import logging
from decimal import Decimal

from ..models.order import Order, LineItem

logger = logging.getLogger(__name__)

class ShopifyDataTransformer:
    """Transforms Shopify order data into database-ready format"""

    @staticmethod
    def _convert_money_to_decimal(money_str: str) -> Decimal:
        """
        Convert money string to Decimal
        
        Args:
            money_str: Money string (e.g., "199.00")
            
        Returns:
            Decimal value
        """
        try:
            return Decimal(money_str)
        except Exception as e:
            logger.error(f"Error converting money string {money_str}: {str(e)}")
            return Decimal('0.00')

    def transform_order(self, order: Order) -> Dict[str, Any]:
        """
        Transform a single order into database format
        
        Args:
            order: Order object to transform
            
        Returns:
            Dictionary with order data ready for database insertion
        """
        try:
            return {
                'id': order.id,
                'name': order.name or '',
                'email': order.email or '',
                'created_at': order.created_at,
                'updated_at': order.updated_at,
                'processed_at': order.processed_at,
                'total_price': self._convert_money_to_decimal(order.total_price),
                'subtotal_price': self._convert_money_to_decimal(order.subtotal_price),
                'total_tax': self._convert_money_to_decimal(order.total_tax),
                'total_discounts': self._convert_money_to_decimal(order.total_discounts),
                'currency': order.currency or '',
                'financial_status': order.financial_status or '',
                'fulfillment_status': order.fulfillment_status or '',
                'customer_id': order.customer.id if order.customer else 0,
                'customer_email': order.customer.email if order.customer else '',
                'customer_first_name': order.customer.first_name if order.customer else '',
                'customer_last_name': order.customer.last_name if order.customer else '',
                'customer_phone': order.customer.phone if order.customer else '',
                'billing_address_city': order.billing_address.city if order.billing_address else '',
                'billing_address_province': order.billing_address.province if order.billing_address else '',
                'billing_address_country': order.billing_address.country if order.billing_address else '',
                'shipping_address_city': order.shipping_address.city if order.shipping_address else '',
                'shipping_address_province': order.shipping_address.province if order.shipping_address else '',
                'shipping_address_country': order.shipping_address.country if order.shipping_address else '',
                'note': order.note or '',
                'tags': order.tags or ''
            }
        except Exception as e:
            logger.error(f"Error transforming order {order.id}: {str(e)}")
            raise

    def transform_order_items(self, order: Order) -> List[Dict[str, Any]]:
        """
        Transform order items from an order into database format
        
        Args:
            order: Order object containing order items
            
        Returns:
            List of dictionaries with order item data ready for database insertion
        """
        try:
            return [
                {
                    'id': item.id,
                    'order_id': order.id,
                    'name': item.name or '',
                    'price': self._convert_money_to_decimal(item.price),
                    'quantity': item.quantity or 0,
                    'sku': item.sku or '',
                    'title': item.title or '',
                    'variant_id': item.variant_id or 0,
                    'product_id': item.product_id or 0,
                    'total_discount': self._convert_money_to_decimal(item.total_discount)
                }
                for item in order.line_items
            ]
        except Exception as e:
            logger.error(f"Error transforming order items for order {order.id}: {str(e)}")
            raise

    def transform_orders(self, orders: List[Order]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """
        Transform multiple orders and their order items
        
        Args:
            orders: List of Order objects to transform
            
        Returns:
            Tuple of (transformed_orders, transformed_order_items)
        """
        transformed_orders = []
        transformed_order_items = []
        
        for order in orders:
            try:
                transformed_orders.append(self.transform_order(order))
                transformed_order_items.extend(self.transform_order_items(order))
            except Exception as e:
                logger.error(f"Error transforming order {order.id}: {str(e)}")
                continue
        
        logger.info(f"Successfully transformed {len(transformed_orders)} orders and {len(transformed_order_items)} order items")
        return transformed_orders, transformed_order_items 