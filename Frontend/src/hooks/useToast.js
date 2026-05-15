/**
 * hooks/useToast.js
 * Lightweight toast notification manager.
 */

import { useState, useCallback } from "react";

export function useToast() {
  const [toast, setToast] = useState(null); // { msg, type }

  const show = useCallback((msg, type = "success", duration = 3500) => {
    setToast({ msg, type });
    setTimeout(() => setToast(null), duration);
  }, []);

  const hide = useCallback(() => setToast(null), []);

  return { toast, show, hide };
}
