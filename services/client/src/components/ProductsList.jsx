import React from 'react';


const ProductsList = (props) => {
  return (
    <div>
      <table className="table is-narrow is-striped is-fullwidth is-hoverable">
      <thead>
        <tr>
          <th>Nombre</th>
          <th>Precio</th>
          <th>Cantidad</th>
          <th>Descripcion</th>
          <th>Categoria</th>
        </tr>
      </thead>
      <tbody>
      {
        props.products.map((product) => {
          return (
            <tr key={product.id}>
            <td>{ product.nombre}</td>
            <td>{ product.precio}</td>
            <td>{ product.cantidad}</td>
            <td>{ product.descripcion}</td>
            <td>{ product.categoria}</td>
            </tr>
          )
        })
      }
      </tbody>
      </table>
    </div>
  )
};


export default ProductsList;