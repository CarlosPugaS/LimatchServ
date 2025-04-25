import React from "react";
import {
  Navbar,
  MobileNav,
  Typography,
  Button,
  IconButton,
} from "@material-tailwind/react";

export default function StickyNavbar() {
  const [openNav, setOpenNav] = React.useState(false);

  React.useEffect(() => {
    window.addEventListener(
      "resize",
      () => window.innerWidth >= 960 && setOpenNav(false),
    );
  }, []);

  const navList = (
    <ul className="mt-2 mb-4 flex flex-col gap-2 lg:mb-0 lg:mt-0 lg:flex-row lg:items-center lg:gap-6">
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal"
      >
        <a href="#" className="flex items-center font-ConcertOne text-[15px] text-txto">
          Inicio
        </a>
      </Typography>
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal"
      >
        <a href="#" className="flex items-center font-ConcertOne text-[15px] text-txto">
          Servicios
        </a>
      </Typography>
      <Typography
        as="li"
        variant="small"
        color="blue-gray"
        className="p-1 font-normal"
      >
        <a href="#" className="flex items-center font-ConcertOne text-[15px] text-txto">
          Contactos
        </a>
      </Typography>

    </ul>
  );

  return (
    <div className="w-full m-0 p-0 rounded-none bg-primario border-none">
      <Navbar className="sticky top-0 z-10 max-w-full border-none rounded-none px-4 py-2 bg-pri">
        <div className="flex items-center justify-between text-blue-gray-900">
        <Typography
          as="a"
          href="#"
          className="flex items-center gap-2 tracking-wide mr-4 cursor-pointer py-2 px-4 text-[30px] font-bold font-ConcertOne bg-gradient-to-r from-start to-end bg-clip-text text-transparent">
          LimatchServ
        </Typography>
          <div className="flex items-center gap-4">
            <div className="mr-4 hidden lg:block">{navList}</div>
            <div className="flex items-center gap-x-1">
              <Button
                className="hidden lg:inline-block text-black font-barlow rounded-none border-1 focus:outline-none bg-end border-gray-200 hover:bg-pri hover:text-ter focus:z-10 focus:ring-4 focus:ring-gray-100">
                <span>Acceder</span>
              </Button>
              <Button
                className="hidden lg:inline-block text-black font-barlow rounded-none border-1 focus:outline-none bg-end border-gray-200 hover:bg-pri hover:text-ter focus:z-10 focus:ring-4 focus:ring-gray-100"
              >
                <span>Regístrate</span>
              </Button>
            </div>
            <IconButton
              variant="text"
              className="ml-auto h-6 w-6 text-inherit hover:bg-transparent focus:bg-transparent active:bg-transparent lg:hidden"
              ripple={false}
              onClick={() => setOpenNav(!openNav)}
            >
              {openNav ? (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  className="h-6 w-6"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              ) : (
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth={2}
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M4 6h16M4 12h16M4 18h16"
                  />
                </svg>
              )}
            </IconButton>
          </div>
        </div>
        <MobileNav open={openNav}>
          {navList}
          <div className="flex items-center gap-x-1">
            <Button fullWidth variant="text" size="sm" className="text-white font-barlow rounded-none bg-ter border-gray-200 hover:bg-pri hover:rounded-none hover:text-ter focus:z-10 focus:ring-0 focus:ring-gray-100 focus:outline-none">
              <span>Regístrate</span>
            </Button>
            <Button fullWidth variant="text" size="sm" className="text-white font-barlow rounded-none bg-ter border-gray-200 hover:bg-pri hover:rounded-none hover:text-ter focus:z-10 focus:ring-0 focus:ring-gray-100 focus:outline-none">
              <span>Acceder</span>
            </Button>
          </div>
        </MobileNav>
      </Navbar>
    </div>
  );
}