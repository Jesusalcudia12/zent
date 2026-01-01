const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// Función para crear una suscripción para un nuevo usuario de ZENT
async function createZentSubscription(customerId, priceId) {
  try {
    const subscription = await stripe.subscriptions.create({
      customer: customerId,
      items: [{ price: priceId }],
      payment_behavior: 'default_incomplete',
      expand: ['latest_invoice.payment_intent'],
    });
    
    return {
      subscriptionId: subscription.id,
      clientSecret: subscription.latest_invoice.payment_intent.client_secret,
    };
  } catch (error) {
    console.error("Error en el pago de ZENT:", error.message);
  }
}
