import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { camelize, getCurrentInstance, toHandlerKey } from 'vue'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const formatTimer = (time: number) => {
  let seconds = time / 1000
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  const twoDecimalSeconds = remainingSeconds.toFixed(2).padStart(5, '0')

  return `${String(minutes).padStart(2, '0')}:${twoDecimalSeconds}`
}
