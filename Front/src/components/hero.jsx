export default function Hero() {
  return (
    <section className="bg-txto flex flex-1 min-h-full flex-col items-center justify-center text-center px-4">
      <div className="py-16 px-4 mx-auto max-w-screen-xl text-center lg:py-24 lg:px-12">
        <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-tight text-pri md:text-5xl lg:text-6xl font-barlow">
          Conecta con prestadores de confianza en Limache
        </h1>
        <p className="mb-8 text-lg font-normal text-seg lg:text-xl sm:px-16 xl:px-48">
          Servicios verificados, agendamiento rápido y apoyo a la economía local. Todo en un solo lugar.
        </p>
        <div className="flex flex-col mb-8 lg:mb-16 space-y-4 sm:flex-row sm:justify-center sm:space-y-0 sm:space-x-4">
          <a
            href="#"
            className="inline-flex justify-center items-center py-3 px-6 text-base font-medium text-pri border border-ter rounded-md hover:bg-ter hover:text-white transition"
          >
            Contrata Ahora
          </a>
          <a
            href="#"
            className="inline-flex justify-center items-center py-3 px-6 text-base font-medium text-pri border border-ter rounded-md hover:bg-ter hover:text-white transition"
          >
            Ser contratado
          </a>
        </div>
      </div>
    </section>
  );
}
