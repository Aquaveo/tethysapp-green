<?xml version="1.0" encoding="UTF-8"?>
<sld:StyledLayerDescriptor xmlns="http://www.opengis.net/sld" xmlns:sld="http://www.opengis.net/sld" xmlns:ogc="http://www.opengis.net/ogc" xmlns:gml="http://www.opengis.net/gml" version="1.0.0">
  <sld:NamedLayer>
    <sld:Name>link_node_dataset</sld:Name>
    <sld:UserStyle>
      <sld:Name>Link Node Dataset</sld:Name>
      <sld:Title>Link Node Dataset</sld:Title>
      <sld:Abstract>A generic style for GSSHA link node datasets</sld:Abstract>
      <sld:FeatureTypeStyle>
        <sld:Name>link_node_dataset</sld:Name>

        <sld:Rule>
          <sld:Title>Rule 1</sld:Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsLessThan>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:Function name="env">
                  <ogc:Literal>division1</ogc:Literal>
                  <ogc:Literal>{{ division1_default|default('0.01') }}</ogc:Literal>
                </ogc:Function>
              </ogc:PropertyIsLessThan>
            </ogc:And>
          </ogc:Filter>
          <sld:PointSymbolizer>
            <sld:Graphic>
              <sld:Mark>
                <sld:WellKnownName>circle</sld:WellKnownName>
                <sld:Fill>
                  <sld:CssParameter name="fill">
                    <ogc:Function name="env">
                      <ogc:Literal>color1</ogc:Literal>
                      <ogc:Literal>#77239D</ogc:Literal>
                    </ogc:Function>
                  </sld:CssParameter>
                </sld:Fill>
              </sld:Mark>
              <sld:Size>6</sld:Size>
            </sld:Graphic>
          </sld:PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              <PropertyName>{{ label_property }}</PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
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
        </sld:Rule>

        <sld:Rule>
          <sld:Title>Rule 2</sld:Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsBetween>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:LowerBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division1</ogc:Literal>
                    <ogc:Literal>{{ division1_default|default('0.01') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:LowerBoundary>
                <ogc:UpperBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division2</ogc:Literal>
                    <ogc:Literal>{{ division2_default|default('0.1') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:UpperBoundary>
              </ogc:PropertyIsBetween>
            </ogc:And>
          </ogc:Filter>
          <sld:PointSymbolizer>
            <sld:Graphic>
              <sld:Mark>
                <sld:WellKnownName>circle</sld:WellKnownName>
                <sld:Fill>
                  <sld:CssParameter name="fill">
                    <ogc:Function name="env">
                      <ogc:Literal>color2</ogc:Literal>
                      <ogc:Literal>#391B95</ogc:Literal>
                    </ogc:Function>
                  </sld:CssParameter>
                </sld:Fill>
              </sld:Mark>
              <sld:Size>6</sld:Size>
            </sld:Graphic>
          </sld:PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              <PropertyName>{{ label_property }}</PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
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
        </sld:Rule>

        <sld:Rule>
          <sld:Title>Rule 3</sld:Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsBetween>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:LowerBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division2</ogc:Literal>
                    <ogc:Literal>{{ division2_default|default('0.1') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:LowerBoundary>
                <ogc:UpperBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division3</ogc:Literal>
                    <ogc:Literal>{{ division3_default|default('1.0') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:UpperBoundary>
              </ogc:PropertyIsBetween>
            </ogc:And>
          </ogc:Filter>
          <sld:PointSymbolizer>
            <sld:Graphic>
              <sld:Mark>
                <sld:WellKnownName>circle</sld:WellKnownName>
                <sld:Fill>
                  <sld:CssParameter name="fill">
                    <ogc:Function name="env">
                      <ogc:Literal>color3</ogc:Literal>
                      <ogc:Literal>#0057D5</ogc:Literal>
                    </ogc:Function>
                  </sld:CssParameter>
                </sld:Fill>
              </sld:Mark>
              <sld:Size>6</sld:Size>
            </sld:Graphic>
          </sld:PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              <PropertyName>{{ label_property }}</PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
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
        </sld:Rule>

        <sld:Rule>
          <sld:Title>Rule 4</sld:Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsBetween>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:LowerBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division3</ogc:Literal>
                    <ogc:Literal>{{ division3_default|default('1.0') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:LowerBoundary>
                <ogc:UpperBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division4</ogc:Literal>
                    <ogc:Literal>{{ division4_default|default('2.0') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:UpperBoundary>
              </ogc:PropertyIsBetween>
            </ogc:And>
          </ogc:Filter>
          <sld:PointSymbolizer>
            <sld:Graphic>
              <sld:Mark>
                <sld:WellKnownName>circle</sld:WellKnownName>
                <sld:Fill>
                  <sld:CssParameter name="fill">
                    <ogc:Function name="env">
                      <ogc:Literal>color4</ogc:Literal>
                      <ogc:Literal>#038DBB</ogc:Literal>
                    </ogc:Function>
                  </sld:CssParameter>
                </sld:Fill>
              </sld:Mark>
              <sld:Size>6</sld:Size>
            </sld:Graphic>
          </sld:PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              <PropertyName>{{ label_property }}</PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
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
        </sld:Rule>

        <sld:Rule>
          <sld:Title>Rule 5</sld:Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsBetween>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:LowerBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division4</ogc:Literal>
                    <ogc:Literal>{{ division4_default|default('2.0') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:LowerBoundary>
                <ogc:UpperBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division5</ogc:Literal>
                    <ogc:Literal>{{ division5_default|default('3.0') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:UpperBoundary>
              </ogc:PropertyIsBetween>
            </ogc:And>
          </ogc:Filter>
          <sld:PointSymbolizer>
            <sld:Graphic>
              <sld:Mark>
                <sld:WellKnownName>circle</sld:WellKnownName>
                <sld:Fill>
                  <sld:CssParameter name="fill">
                    <ogc:Function name="env">
                      <ogc:Literal>color5</ogc:Literal>
                      <ogc:Literal>#649C31</ogc:Literal>
                    </ogc:Function>
                  </sld:CssParameter>
                </sld:Fill>
              </sld:Mark>
              <sld:Size>6</sld:Size>
            </sld:Graphic>
          </sld:PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              <PropertyName>{{ label_property }}</PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
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
        </sld:Rule>

        <sld:Rule>
          <sld:Title>Rule 6</sld:Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsBetween>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:LowerBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division5</ogc:Literal>
                    <ogc:Literal>{{ division5_default|default('3.0') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:LowerBoundary>
                <ogc:UpperBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division6</ogc:Literal>
                    <ogc:Literal>{{ division6_default|default('4.0') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:UpperBoundary>
              </ogc:PropertyIsBetween>
            </ogc:And>
          </ogc:Filter>
          <sld:PointSymbolizer>
            <sld:Graphic>
              <sld:Mark>
                <sld:WellKnownName>circle</sld:WellKnownName>
                <sld:Fill>
                  <sld:CssParameter name="fill">
                    <ogc:Function name="env">
                      <ogc:Literal>color6</ogc:Literal>
                      <ogc:Literal>#F4ED01</ogc:Literal>
                    </ogc:Function>
                  </sld:CssParameter>
                </sld:Fill>
              </sld:Mark>
              <sld:Size>6</sld:Size>
            </sld:Graphic>
          </sld:PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              <PropertyName>{{ label_property }}</PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
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
        </sld:Rule>

        <sld:Rule>
          <sld:Title>Rule 7</sld:Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsBetween>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:LowerBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division6</ogc:Literal>
                    <ogc:Literal>{{ division6_default|default('4.0') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:LowerBoundary>
                <ogc:UpperBoundary>
                  <ogc:Function name="env">
                    <ogc:Literal>division7</ogc:Literal>
                    <ogc:Literal>{{ division7_default|default('5.0') }}</ogc:Literal>
                  </ogc:Function>
                </ogc:UpperBoundary>
              </ogc:PropertyIsBetween>
            </ogc:And>
          </ogc:Filter>
          <sld:PointSymbolizer>
            <sld:Graphic>
              <sld:Mark>
                <sld:WellKnownName>circle</sld:WellKnownName>
                <sld:Fill>
                  <sld:CssParameter name="fill">
                    <ogc:Function name="env">
                      <ogc:Literal>color7</ogc:Literal>
                      <ogc:Literal>#D38306</ogc:Literal>
                    </ogc:Function>
                  </sld:CssParameter>
                </sld:Fill>
              </sld:Mark>
              <sld:Size>6</sld:Size>
            </sld:Graphic>
          </sld:PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              <PropertyName>{{ label_property }}</PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
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
        </sld:Rule>

        <sld:Rule>
          <sld:Title>Rule 8</sld:Title>
          <ogc:Filter>
            <ogc:And>
              <ogc:PropertyIsGreaterThan>
                <ogc:PropertyName>value</ogc:PropertyName>
                <ogc:Function name="env">
                  <ogc:Literal>division7</ogc:Literal>
                  <ogc:Literal>{{ division7_default|default('5.0') }}</ogc:Literal>
                </ogc:Function>
              </ogc:PropertyIsGreaterThan>
            </ogc:And>
          </ogc:Filter>
          <sld:PointSymbolizer>
            <sld:Graphic>
              <sld:Mark>
                <sld:WellKnownName>circle</sld:WellKnownName>
                <sld:Fill>
                  <sld:CssParameter name="fill">
                    <ogc:Function name="env">
                      <ogc:Literal>color8</ogc:Literal>
                      <ogc:Literal>#E12300</ogc:Literal>
                    </ogc:Function>
                  </sld:CssParameter>
                </sld:Fill>
              </sld:Mark>
              <sld:Size>6</sld:Size>
            </sld:Graphic>
          </sld:PointSymbolizer>
          {% if is_label_style %}
          <TextSymbolizer>
            <Label>
              <PropertyName>{{ label_property }}</PropertyName>
              <ogc:Function name="env">
                <ogc:Literal>units</ogc:Literal>
                <ogc:Literal></ogc:Literal>
              </ogc:Function>
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
        </sld:Rule>
      </sld:FeatureTypeStyle>
    </sld:UserStyle>
  </sld:NamedLayer>
</sld:StyledLayerDescriptor>
