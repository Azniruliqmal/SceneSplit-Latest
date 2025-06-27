import { useProjectStore } from '../stores/projectStore'
import { useRouter } from 'vue-router'

export function useAuth() {
  const store = useProjectStore()
  const router = useRouter()

  function login(email: string, password: string) {
    if (email === 'admin@email.com' && password === 'password') {
      store.setLogin(true)
      router.push({ name: 'ProjectsView' })
      return true
    }
    return false
  }

  function logout() {
    store.setLogin(false)
    router.push({ name: 'Login' })
  }

  return { login, logout, isLoggedIn: store.isLoggedIn }
}