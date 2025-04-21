function Navbar() {
  return (
    <nav className="bg-white shadow p-4">
    <div className="container mx-auto flex justify-between items-center">
      <h1 className="text-xl font-bold text-indigo-600">LimatchServ 🍅</h1>
      <ul className="flex gap-4 text-sm">
        <li><a href="/" className="hover:text-indigo-600">Inicio</a></li>
        <li><a href="/login" className="hover:text-indigo-600">Iniciar Sesión</a></li>
        <li><a href="/register" className="hover:text-indigo-600">Registrarse</a></li>
      </ul>
    </div>
  </nav>
  )
}

export default Navbar;