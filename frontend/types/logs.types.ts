export enum LogLevels {
  DEBUG = 'DEBUG',
  INFO = 'INFO',
  WARNING = 'WARNING',
  ERROR = 'ERROR',
  CRITICAL = 'CRITICAL'
}

export interface LogLine {
  time: string
  level: LogLevels
  message: string
}
