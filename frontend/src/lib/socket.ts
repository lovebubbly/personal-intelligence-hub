"use client";

import { io, Socket } from "socket.io-client";

const SOCKET_BASE = process.env.NEXT_PUBLIC_SOCKET_BASE_URL ?? "http://localhost:8000";
const NAMESPACE = process.env.NEXT_PUBLIC_SOCKET_NAMESPACE ?? "/feed";

let socket: Socket | null = null;

export function getFeedSocket(): Socket {
  if (socket) {
    return socket;
  }

  socket = io(`${SOCKET_BASE}${NAMESPACE}`, {
    transports: ["websocket"],
    reconnection: true,
    reconnectionAttempts: 10,
    reconnectionDelay: 1200
  });

  return socket;
}
