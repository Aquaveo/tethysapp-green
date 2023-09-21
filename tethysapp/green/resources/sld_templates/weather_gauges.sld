<?xml version="1.0" encoding="ISO-8859-1"?>
<StyledLayerDescriptor version="1.0.0"
 xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
 xmlns="http://www.opengis.net/sld"
 xmlns:ogc="http://www.opengis.net/ogc"
 xmlns:xlink="http://www.w3.org/1999/xlink"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <!-- a Named Layer is the basic building block of an SLD document -->
  <NamedLayer>
    <Name>stream_gauges</Name>
    <UserStyle>
    <!-- Styles can have names, titles and abstracts -->
      <Title>Stream Gauges</Title>
      <Abstract>GSSHA Stream Gauges</Abstract>
      <!-- FeatureTypeStyles describe how to render different features -->
      <!-- A FeatureTypeStyle for rendering points -->
      <FeatureTypeStyle>
        <Rule>
          <Name>&lt;2 year</Name>
          <Title>&lt;2 year</Title>
          <Abstract>Return period of less than 2 years</Abstract>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:PropertyIsLessThan>
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
              <ogc:Literal>2.0</ogc:Literal>
            </ogc:PropertyIsLessThan>
          </ogc:Filter>
            <PointSymbolizer>
              <Graphic>
                <Mark>
                  <WellKnownName>square</WellKnownName>
                  <Fill>
                    <CssParameter name="fill">#2154ff</CssParameter>
                  </Fill>
                  <Stroke>
                    <CssParameter name="stroke">#f6f3ee</CssParameter>
                    <CssParameter name="stroke-width">0.5</CssParameter>
                  </Stroke>
                </Mark>
              <Size>16</Size>
            </Graphic>
          </PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              {% if is_name_style %}
              <ogc:PropertyName>name</ogc:PropertyName>
              {% else %}
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
              {% endif %}
            </Label>
            <Font>
              <CssParameter name="font-size">12</CssParameter>
            </Font>
            <LabelPlacement>
              <PointPlacement>
                <AnchorPoint>
                  <AnchorPointX>0.5</AnchorPointX>
                  <AnchorPointY>0.0</AnchorPointY>
                </AnchorPoint>
                <Displacement>
                  <DisplacementX>0</DisplacementX>
                  <DisplacementY>5</DisplacementY>
                </Displacement>
              </PointPlacement>
            </LabelPlacement>
            <Halo>
              <Radius>3</Radius>
              <Fill>
                <CssParameter name="fill-opacity">0.9</CssParameter>
                <CssParameter name="fill">#FFFFFF</CssParameter>
              </Fill>
            </Halo>
          </TextSymbolizer>
          {% endif %}
        </Rule>
        <Rule>
          <Name>2 year</Name>
          <Title>2 year</Title>
          <Abstract>Return period of 2-5 years</Abstract>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>2.0</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>5.0</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
            <PointSymbolizer>
              <Graphic>
                <Mark>
                  <WellKnownName>square</WellKnownName>
                  <Fill>
                    <CssParameter name="fill">#00c1ff</CssParameter>
                  </Fill>
                  <Stroke>
                    <CssParameter name="stroke">#f6f3ee</CssParameter>
                    <CssParameter name="stroke-width">0.5</CssParameter>
                  </Stroke>
                </Mark>
              <Size>16</Size>
            </Graphic>
          </PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              {% if is_name_style %}
              <ogc:PropertyName>name</ogc:PropertyName>
              {% else %}
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
              {% endif %}
            </Label>
            <Font>
              <CssParameter name="font-size">12</CssParameter>
            </Font>
            <LabelPlacement>
              <PointPlacement>
                <AnchorPoint>
                  <AnchorPointX>0.5</AnchorPointX>
                  <AnchorPointY>0.0</AnchorPointY>
                </AnchorPoint>
                <Displacement>
                  <DisplacementX>0</DisplacementX>
                  <DisplacementY>5</DisplacementY>
                </Displacement>
              </PointPlacement>
            </LabelPlacement>
            <Halo>
              <Radius>3</Radius>
              <Fill>
                <CssParameter name="fill-opacity">0.9</CssParameter>
                <CssParameter name="fill">#FFFFFF</CssParameter>
              </Fill>
            </Halo>
          </TextSymbolizer>
          {% endif %}
        </Rule>
        <Rule>
          <Name>5 year</Name>
          <Title>5 year</Title>
          <Abstract>Return period of 5-10 years</Abstract>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>5.0</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>10.0</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
            <PointSymbolizer>
              <Graphic>
                <Mark>
                  <WellKnownName>square</WellKnownName>
                  <Fill>
                    <CssParameter name="fill">#57ffd4</CssParameter>
                  </Fill>
                  <Stroke>
                    <CssParameter name="stroke">#f6f3ee</CssParameter>
                    <CssParameter name="stroke-width">0.5</CssParameter>
                  </Stroke>
                </Mark>
              <Size>16</Size>
            </Graphic>
          </PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              {% if is_name_style %}
              <ogc:PropertyName>name</ogc:PropertyName>
              {% else %}
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
              {% endif %}
            </Label>
            <Font>
              <CssParameter name="font-size">12</CssParameter>
            </Font>
            <LabelPlacement>
              <PointPlacement>
                <AnchorPoint>
                  <AnchorPointX>0.5</AnchorPointX>
                  <AnchorPointY>0.0</AnchorPointY>
                </AnchorPoint>
                <Displacement>
                  <DisplacementX>0</DisplacementX>
                  <DisplacementY>5</DisplacementY>
                </Displacement>
              </PointPlacement>
            </LabelPlacement>
            <Halo>
              <Radius>3</Radius>
              <Fill>
                <CssParameter name="fill-opacity">0.9</CssParameter>
                <CssParameter name="fill">#FFFFFF</CssParameter>
              </Fill>
            </Halo>
          </TextSymbolizer>
          {% endif %}
        </Rule>
        <Rule>
          <Name>10 year</Name>
          <Title>10 year</Title>
          <Abstract>Return period of 10-25 years</Abstract>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>10.0</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>25.0</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
            <PointSymbolizer>
              <Graphic>
                <Mark>
                  <WellKnownName>square</WellKnownName>
                  <Fill>
                    <CssParameter name="fill">#028f37</CssParameter>
                  </Fill>
                  <Stroke>
                    <CssParameter name="stroke">#f6f3ee</CssParameter>
                    <CssParameter name="stroke-width">0.5</CssParameter>
                  </Stroke>
                </Mark>
              <Size>16</Size>
            </Graphic>
          </PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              {% if is_name_style %}
              <ogc:PropertyName>name</ogc:PropertyName>
              {% else %}
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
              {% endif %}
            </Label>
            <Font>
              <CssParameter name="font-size">12</CssParameter>
            </Font>
            <LabelPlacement>
              <PointPlacement>
                <AnchorPoint>
                  <AnchorPointX>0.5</AnchorPointX>
                  <AnchorPointY>0.0</AnchorPointY>
                </AnchorPoint>
                <Displacement>
                  <DisplacementX>0</DisplacementX>
                  <DisplacementY>5</DisplacementY>
                </Displacement>
              </PointPlacement>
            </LabelPlacement>
            <Halo>
              <Radius>3</Radius>
              <Fill>
                <CssParameter name="fill-opacity">0.9</CssParameter>
                <CssParameter name="fill">#FFFFFF</CssParameter>
              </Fill>
            </Halo>
          </TextSymbolizer>
          {% endif %}
        </Rule>
        <Rule>
          <Name>25 year</Name>
          <Title>25 year</Title>
          <Abstract>Return period of 25-50 years</Abstract>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>25.0</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>50.0</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
            <PointSymbolizer>
              <Graphic>
                <Mark>
                  <WellKnownName>square</WellKnownName>
                  <Fill>
                    <CssParameter name="fill">#4eb600</CssParameter>
                  </Fill>
                  <Stroke>
                    <CssParameter name="stroke">#f6f3ee</CssParameter>
                    <CssParameter name="stroke-width">0.5</CssParameter>
                  </Stroke>
                </Mark>
              <Size>16</Size>
            </Graphic>
          </PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              {% if is_name_style %}
              <ogc:PropertyName>name</ogc:PropertyName>
              {% else %}
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
              {% endif %}
            </Label>
            <Font>
              <CssParameter name="font-size">12</CssParameter>
            </Font>
            <LabelPlacement>
              <PointPlacement>
                <AnchorPoint>
                  <AnchorPointX>0.5</AnchorPointX>
                  <AnchorPointY>0.0</AnchorPointY>
                </AnchorPoint>
                <Displacement>
                  <DisplacementX>0</DisplacementX>
                  <DisplacementY>5</DisplacementY>
                </Displacement>
              </PointPlacement>
            </LabelPlacement>
            <Halo>
              <Radius>3</Radius>
              <Fill>
                <CssParameter name="fill-opacity">0.9</CssParameter>
                <CssParameter name="fill">#FFFFFF</CssParameter>
              </Fill>
            </Halo>
          </TextSymbolizer>
          {% endif %}
        </Rule>
        <Rule>
          <Name>50 year</Name>
          <Title>50 year</Title>
          <Abstract>Return period of 50-100 years</Abstract>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>50.0</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>100.0</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
            <PointSymbolizer>
              <Graphic>
                <Mark>
                  <WellKnownName>square</WellKnownName>
                  <Fill>
                    <CssParameter name="fill">#fffa01</CssParameter>
                  </Fill>
                  <Stroke>
                    <CssParameter name="stroke">#f6f3ee</CssParameter>
                    <CssParameter name="stroke-width">0.5</CssParameter>
                  </Stroke>
                </Mark>
              <Size>16</Size>
            </Graphic>
          </PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              {% if is_name_style %}
              <ogc:PropertyName>name</ogc:PropertyName>
              {% else %}
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
              {% endif %}
            </Label>
            <Font>
              <CssParameter name="font-size">12</CssParameter>
            </Font>
            <LabelPlacement>
              <PointPlacement>
                <AnchorPoint>
                  <AnchorPointX>0.5</AnchorPointX>
                  <AnchorPointY>0.0</AnchorPointY>
                </AnchorPoint>
                <Displacement>
                  <DisplacementX>0</DisplacementX>
                  <DisplacementY>5</DisplacementY>
                </Displacement>
              </PointPlacement>
            </LabelPlacement>
            <Halo>
              <Radius>3</Radius>
              <Fill>
                <CssParameter name="fill-opacity">0.9</CssParameter>
                <CssParameter name="fill">#FFFFFF</CssParameter>
              </Fill>
            </Halo>
          </TextSymbolizer>
          {% endif %}
        </Rule>
        <Rule>
          <Name>100 year</Name>
          <Title>100 year</Title>
          <Abstract>Return period of 100-200 years</Abstract>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>100.0</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>200.0</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
            <PointSymbolizer>
              <Graphic>
                <Mark>
                  <WellKnownName>square</WellKnownName>
                  <Fill>
                    <CssParameter name="fill">#ffa500</CssParameter>
                  </Fill>
                  <Stroke>
                    <CssParameter name="stroke">#f6f3ee</CssParameter>
                    <CssParameter name="stroke-width">0.5</CssParameter>
                  </Stroke>
                </Mark>
              <Size>16</Size>
            </Graphic>
          </PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              {% if is_name_style %}
              <ogc:PropertyName>name</ogc:PropertyName>
              {% else %}
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
              {% endif %}
            </Label>
            <Font>
              <CssParameter name="font-size">12</CssParameter>
            </Font>
            <LabelPlacement>
              <PointPlacement>
                <AnchorPoint>
                  <AnchorPointX>0.5</AnchorPointX>
                  <AnchorPointY>0.0</AnchorPointY>
                </AnchorPoint>
                <Displacement>
                  <DisplacementX>0</DisplacementX>
                  <DisplacementY>5</DisplacementY>
                </Displacement>
              </PointPlacement>
            </LabelPlacement>
            <Halo>
              <Radius>3</Radius>
              <Fill>
                <CssParameter name="fill-opacity">0.9</CssParameter>
                <CssParameter name="fill">#FFFFFF</CssParameter>
              </Fill>
            </Halo>
          </TextSymbolizer>
          {% endif %}
        </Rule>
        <Rule>
          <Name>200 year</Name>
          <Title>200 year</Title>
          <Abstract>Return period of 200-500 years</Abstract>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:And>
              <ogc:PropertyIsGreaterThanOrEqualTo>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>200.0</ogc:Literal>
              </ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>max_return_period</ogc:PropertyName>
                <ogc:Literal>500.0</ogc:Literal>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
            <PointSymbolizer>
              <Graphic>
                <Mark>
                  <WellKnownName>square</WellKnownName>
                  <Fill>
                    <CssParameter name="fill">#ff0000</CssParameter>
                  </Fill>
                  <Stroke>
                    <CssParameter name="stroke">#f6f3ee</CssParameter>
                    <CssParameter name="stroke-width">0.5</CssParameter>
                  </Stroke>
                </Mark>
              <Size>16</Size>
            </Graphic>
          </PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              {% if is_name_style %}
              <ogc:PropertyName>name</ogc:PropertyName>
              {% else %}
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
              {% endif %}
            </Label>
            <Font>
              <CssParameter name="font-size">12</CssParameter>
            </Font>
            <LabelPlacement>
              <PointPlacement>
                <AnchorPoint>
                  <AnchorPointX>0.5</AnchorPointX>
                  <AnchorPointY>0.0</AnchorPointY>
                </AnchorPoint>
                <Displacement>
                  <DisplacementX>0</DisplacementX>
                  <DisplacementY>5</DisplacementY>
                </Displacement>
              </PointPlacement>
            </LabelPlacement>
            <Halo>
              <Radius>3</Radius>
              <Fill>
                <CssParameter name="fill-opacity">0.9</CssParameter>
                <CssParameter name="fill">#FFFFFF</CssParameter>
              </Fill>
            </Halo>
          </TextSymbolizer>
          {% endif %}
        </Rule>
        <Rule>
          <Name>&gt;500 year</Name>
          <Title>&gt;500 year</Title>
          <Abstract>Return period of greater than 500 years</Abstract>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:PropertyIsGreaterThanOrEqualTo>
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
              <ogc:Literal>500.0</ogc:Literal>
            </ogc:PropertyIsGreaterThanOrEqualTo>
          </ogc:Filter>
            <PointSymbolizer>
              <Graphic>
                <Mark>
                  <WellKnownName>square</WellKnownName>
                  <Fill>
                    <CssParameter name="fill">#b23eff</CssParameter>
                  </Fill>
                  <Stroke>
                    <CssParameter name="stroke">#f6f3ee</CssParameter>
                    <CssParameter name="stroke-width">0.5</CssParameter>
                  </Stroke>
                </Mark>
              <Size>16</Size>
            </Graphic>
          </PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              {% if is_name_style %}
              <ogc:PropertyName>name</ogc:PropertyName>
              {% else %}
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
              {% endif %}
            </Label>
            <Font>
              <CssParameter name="font-size">12</CssParameter>
            </Font>
            <LabelPlacement>
              <PointPlacement>
                <AnchorPoint>
                  <AnchorPointX>0.5</AnchorPointX>
                  <AnchorPointY>0.0</AnchorPointY>
                </AnchorPoint>
                <Displacement>
                  <DisplacementX>0</DisplacementX>
                  <DisplacementY>5</DisplacementY>
                </Displacement>
              </PointPlacement>
            </LabelPlacement>
            <Halo>
              <Radius>3</Radius>
              <Fill>
                <CssParameter name="fill-opacity">0.9</CssParameter>
                <CssParameter name="fill">#FFFFFF</CssParameter>
              </Fill>
            </Halo>
          </TextSymbolizer>
          {% endif %}
        </Rule>
        <Rule>
          <Name>No Data</Name>
          <Title>No Data</Title>
          <Abstract>max_return_period is undefined</Abstract>
          <ogc:Filter xmlns:ogc="http://www.opengis.net/ogc">
            <ogc:PropertyIsNull>
              <ogc:PropertyName>max_return_period</ogc:PropertyName>
            </ogc:PropertyIsNull>
          </ogc:Filter>
          <PointSymbolizer>
              <Graphic>
                <Mark>
                  <WellKnownName>square</WellKnownName>
                  <Fill>
                    <CssParameter name="fill">#000000</CssParameter>
                  </Fill>
                  <Stroke>
                    <CssParameter name="stroke">#f6f3ee</CssParameter>
                    <CssParameter name="stroke-width">0.5</CssParameter>
                  </Stroke>
                </Mark>
              <Size>16</Size>
            </Graphic>
          </PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              {% if is_name_style %}
              <ogc:PropertyName>name</ogc:PropertyName>
              {% else %}
              No Data
              {% endif %}
            </Label>
            <Font>
              <CssParameter name="font-size">12</CssParameter>
            </Font>
            <LabelPlacement>
              <PointPlacement>
                <AnchorPoint>
                  <AnchorPointX>0.5</AnchorPointX>
                  <AnchorPointY>0.0</AnchorPointY>
                </AnchorPoint>
                <Displacement>
                  <DisplacementX>0</DisplacementX>
                  <DisplacementY>5</DisplacementY>
                </Displacement>
              </PointPlacement>
            </LabelPlacement>
            <Halo>
              <Radius>3</Radius>
              <Fill>
                <CssParameter name="fill-opacity">0.9</CssParameter>
                <CssParameter name="fill">#FFFFFF</CssParameter>
              </Fill>
            </Halo>
          </TextSymbolizer>
          {% endif %}
        </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>