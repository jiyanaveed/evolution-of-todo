/**
 * Chat Endpoint - No longer needed as we're calling the backend directly
 * The AIChatBox component now calls the backend API directly
 */
export async function POST(req: Request) {
  // This endpoint is no longer used since we're calling the backend directly
  // from the AIChatBox component
  return new Response('This endpoint is deprecated. Use /api/{user_id}/chat directly.', { status: 400 });
}
