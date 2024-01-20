import { type ClassValue, clsx } from 'clsx'
import { twMerge } from 'tailwind-merge'
import { camelize, getCurrentInstance, toHandlerKey } from 'vue'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export const formatTimer = (time: number) => {
  if (time < 0) return '00:00.00'
  let seconds = time / 100
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  const twoDecimalSeconds = remainingSeconds.toFixed(2).padStart(5, '0')

  return `${String(minutes).padStart(2, '0')}:${twoDecimalSeconds}`
}

export const formatTime = (timestamp: number) => {
  const date = new Date(timestamp * 1000)

  return date.toLocaleString('fr-FR', {
    timeZone: 'Europe/Paris'
  })
}

export const getDurationBetweenTimestampsFormat = (
  start: number,
  end: number
): string => {
  start = start * 1000
  end = end * 1000
  const duration = end - start
  const minutes = Math.floor(duration / 60000)
  const seconds = ((duration % 60000) / 1000).toFixed(0)
  const hours = Math.floor(duration / 3600000)

  return `${hours}h ${minutes}mn ${seconds}s`
}
