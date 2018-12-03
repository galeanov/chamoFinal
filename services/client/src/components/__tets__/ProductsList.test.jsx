import React from 'react';
import { shallow } from 'enzyme';
import renderer from 'react-test-renderer';
 
import ProductsList from '../ProductsList';
 
const products = [
  {
    'active': true,
    'cantidad': 12,
    'precio': 0.12,
    'descripcion': 'esta rico',
    'categoria': 'Galletas',
    'id': 1,
    'nombre': 'soda'
  },
  {
    'active': true,
    'cantidad': 20,
    'precio': 0.7,
    'descripcion': 'esta buenaso',
    'categoria': 'Galletas',
    'id': 2,
    'nombre': 'soda field'
  }
];
 
test('ProductsList renders properly', () => {
  const wrapper = shallow(<ProductsList products={products}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.children).toBe('Oreo');
});

test('ProductsList renders a snapshot properly', () => {
  const tree = renderer.create(<ProductsList products={products}/>).toJSON();
  expect(tree).toMatchSnapshot();
});
