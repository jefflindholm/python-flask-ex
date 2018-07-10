import React from 'react';
import renderer from 'react-test-renderer';
import { shallow } from 'enzyme';

import UsersList from '../components/users-list';

const users = [
  { active: true, email: 'jeff@lindholm.org', id: 1, username: 'jeff' },
  { active: true, email: 'iryna@lindholm.org', id: 2, username: 'iryna' },
];

test('UsersList renders properly', () => {
  const wrapper = shallow(<UsersList users={users}/>);
  const element = wrapper.find('h4');
  expect(element.length).toBe(2);
  expect(element.get(0).props.className).toBe('card card-body bg-light');
  expect(element.get(0).props.children).toBe('jeff');
});

test('UsersList renders correct snapshot', () => {
  const tree = renderer.create(<UsersList users={users}/>).toJSON();
  expect(tree).toMatchSnapshot();
});
