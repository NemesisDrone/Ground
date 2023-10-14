export const useApi: typeof useFetch = (request, opts?) => {
  const config = useRuntimeConfig()
  // @ts-ignore
  return useFetch(request, { baseURL: config.public.API_URL, ...opts })
}
