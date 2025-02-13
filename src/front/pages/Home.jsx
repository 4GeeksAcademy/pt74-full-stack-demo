import { useEffect, useState } from "react";
import useGlobalReducer from "../hooks/useGlobalReducer.jsx";

const SomeComponent = ({ input, onClick }) => {
  return (
    <div onClick={() => onClick(100)}>
      This value will be 100 when you click this: {input}
    </div>
  );
};

export const Home = () => {
  const { store, dispatch } = useGlobalReducer();

  const [value, setValue] = useState(0);

  useEffect(() => {
    console.log("This runs when the component mounts.");
  }, []);

  useEffect(() => {
    console.log("This runs when value updates.");
  }, [value]);

  return (
    <div className="text-center mt-5">
      <button className="btn btn-primary" onClick={() => setValue(value + 1)}>
        ++
      </button>
      <h1>{value}</h1>
      <button className="btn btn-primary" onClick={() => setValue(value - 1)}>
        --
      </button>
      <SomeComponent input={value} onClick={setValue} />
    </div>
  );
};
